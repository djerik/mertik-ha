"""Mertik Wifi Fireplace controller."""

import socket

__version__ = "0.1.0"
__author__ = "Tobias Laursen <djerik@gmail.com>"
__all__ = []

SEND_COMMAND_PREFIX = "0233303330333033303830"
PROCESS_STATUS_PREFIXES = ("303030300003", "030300000003")


class Mertik:
    def __init__(self, ip):
        self.ip = ip
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(3)
        self.client.connect((self.ip, 2000))
        self.refresh_status()

    @staticmethod
    def get_devices():
        # Setup receiver
        udp_port = 30719
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("", udp_port))

        # Send broadcast
        udp_port = 30718
        message = "000100f6"
        hexstring = bytearray.fromhex(message)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(hexstring, ("<broadcast>", udp_port))

        # Receive reply
        data, addr = sock.recvfrom(1024)
        mac = getmacbyip(addr)
        device = {}
        device["address"] = addr
        device["mac"] = mac
        return device

    @property
    def is_on(self) -> bool:
        return self.on

    @property
    def is_aux_on(self) -> bool:
        return self._aux_on

    @property
    def is_shutting_down(self) -> bool:
        return self._shutting_down

    @property
    def is_igniting(self) -> bool:
        return self._igniting

    @property
    def ambient_temperature(self) -> float:
        return self._ambient_temperature

    @property
    def is_light_on(self) -> bool:
        return self._light_on

    @property
    def dim_level(self) -> int:
        return self._dim_level

    def stand_by(self):
        msg = "3136303003"
        self.__send_command(msg)

    def aux_on(self):
        msg = "32303031030a"
        self.__send_command(msg)

    def aux_off(self):
        msg = "32303030030a"
        self.__send_command(msg)

    def ignite_fireplace(self):
        msg = "314103"
        self.__send_command(msg)

    def refresh_status(self):
        msg = "303303"
        self.__send_command(msg)

    def guard_flame_off(self):
        msg = "313003"
        self.__send_command(msg)

    def set_light_dim(self, dim_level):
        level = format(36 + round(9 * dim_level), "02x").upper()
        msg = "33304645" + level + level + "030a"
        self.__send_command(msg)

    def set_eco(self):
        msg = "4233303103"
        self.__send_command(msg)

    def set_manual(self):
        msg = "423003"
        self.__send_command(msg)

    def get_flame_height(self) -> int:
        return self.flame_height

    def set_flame_height(self, flame_height) -> None:
        steps = [
            "3830",
            "3842",
            "3937",
            "4132",
            "4145",
            "4239",
            "4335",
            "4430",
            "4443",
            "4537",
            "4633",
            "4646",
        ]
        step = steps[flame_height - 1]
        msg = "3136" + step + "03"
        self.__send_command(msg)
        self.refresh_status()

    def __hex_to_bin(self, hex_val):
        return format(int(hex_val, 16), "b").zfill(8)

    def __from_bit_status(self, hex_val, index):
        return self.__hex_to_bin(hex_val)[index : index + 1] == "1"

    def close(self) -> None:
        """Close the socket connection."""
        self.client.close()

    def __reconnect(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(3)
        self.client.connect((self.ip, 2000))

    def __send_command(self, msg: str) -> None:
        payload = bytearray.fromhex(SEND_COMMAND_PREFIX + msg)
        try:
            self.client.send(payload)
        except OSError:
            self.__reconnect()
            self.client.send(payload)

        data = self.client.recv(1024)
        if len(data) == 0:
            # Connection was closed by peer — reconnect for next command.
            self.__reconnect()
            return

        temp_data = str(data, "ascii")[1:]
        temp_data = temp_data.replace("\r", ";")
        if temp_data.startswith(PROCESS_STATUS_PREFIXES):
            self.__process_status(temp_data)

    def __process_status(self, status_str):
        temp_sub = "0x" + status_str[14:16]
        flame_height = int(temp_sub, 0)

        if flame_height <= 123:
            self.flame_height = 0
            self.on = False
        else:
            self.flame_height = round(((flame_height - 128) / 128) * 12) + 1
            self.on = True

        status_bits = status_str[16:20]
        self._shutting_down = self.__from_bit_status(status_bits, 7)
        self._guard_flame_on = self.__from_bit_status(status_bits, 8)
        self._igniting = self.__from_bit_status(status_bits, 11)
        self._aux_on = self.__from_bit_status(status_bits, 12)
        self._light_on = self.__from_bit_status(status_bits, 13)

        self._dim_level = (int("0x" + status_str[20:22], 0) - 100) / 151
        if self._dim_level < 0 or not self._light_on:
            self._dim_level = 0

        self._ambient_temperature = int("0x" + status_str[28:32], 0) / 10

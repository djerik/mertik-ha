from re import M
import re
import socket
import struct
import sys
import binascii

# from pytest import console_main

"Mertik Wifi Fireplace controller"

__version__ = "0.1.0"
__author__ = "Tobias Laursen <djerik@gmail.com>"
__all__ = []

send_command_prefix = "0233303330333033303830"
process_status_prefixes = ("303030300003", "030300000003")

class Mertik:
    def __init__(self, ip):
        self.ip = ip
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Internet
        self.client.settimeout(3)
        self.client.connect((self.ip, 2000))
        self.refresh_status()

    def get_devices():
        # Setup receiver
        UDP_PORT = 30719
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
        sock.bind(("", UDP_PORT))

        # Send broadcast
        UDP_PORT = 30718
        MESSAGE = "000100f6"
        hexstring = bytearray.fromhex(MESSAGE)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(hexstring, ("<broadcast>", 30718))

        # Receive reply
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        mac = getmacbyip(addr)
        device = dict()
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
    def light_brightness(self) -> int:
        return self._light_brightness

    def standBy(self):
        msg = "3136303003"
        self.__sendCommand(msg)

    def aux_on(self):
        # this.getDriver().triggerDualFlameToggle.trigger(this, {}, {});
        # this.getDriver().triggerDualFlameOn.trigger(this, {}, {});
        msg = "32303031030a"
        self.__sendCommand(msg)

    def aux_off(self):
        # this.getDriver().triggerDualFlameToggle.trigger(this, {}, {});
        # this.getDriver().triggerDualFlameOff.trigger(this, {}, {});
        msg = "32303030030a"
        self.__sendCommand(msg)

    def ignite_fireplace(self):
        msg = "314103"
        self.__sendCommand(msg)

    def refresh_status(self):
        msg = "303303"
        self.__sendCommand(msg)

    def guard_flame_off(self):
        msg = "313003"
        self.__sendCommand(msg)

    def light_on(self):
        msg = "3330303103"
        self.__sendCommand(msg)

    def light_off(self):
        msg = "3330303003"
        self.__sendCommand(msg)

    def set_light_brightness(self, brightness) -> None:
        if brightness is None:
            self.light_on()
            return

        l = 36 + round((brightness / 255) * 10)
        if l >= 40:
            l += 1 # For some reason 40 should be skipped..?

        msg = "33304645" + str(l) + str(l) + "030a"
        self.__sendCommand(msg)

    def set_eco(self):
        msg = "4233303103"
        self.__sendCommand(msg)

    def set_manual(self):
        msg = "423003"
        self.__sendCommand(msg)

    def get_flame_height(self) -> int:
        return self.flameHeight

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
        l = steps[flame_height - 1]
        msg = "3136" + l + "03"

        self.__sendCommand(msg)

    def __hex2bin(self, hex):
        return format(int(hex, 16), "b").zfill(8)

    def __fromBitStatus(self, hex, index):
        return self.__hex2bin(hex)[index : index + 1] == "1"

    def __sendCommand(self, msg):
        try:
            self.client.send(bytearray.fromhex(send_command_prefix + msg))
        except socket.error:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.ip, 2000))
            self.client.send(bytearray.fromhex(send_command_prefix + msg))

        data = self.client.recv(1024)
        if len(data) == 0:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.ip, 2000))
            self.client.send(bytearray.fromhex(send_command_prefix + msg))
            data = self.client.recv(1024)

        tempData = str(data, "ascii")
        tempData = tempData[1:]
        tempData = re.sub("/\r/g", ";", tempData)
        if tempData.startswith(process_status_prefixes):
            self.__processStatus(tempData)

    def __processStatus(self, statusStr):
        tempSub = statusStr[14:16]
        tempSub = "0x" + tempSub
        flameHeight = int(tempSub, 0)

        if flameHeight <= 123:
            self.flameHeight = 0
            self.on = False
        else:
            self.flameHeight = round(((flameHeight - 128) / 128) * 12) + 1
            self.on = True

        mode = statusStr[24:25]
        statusBits = statusStr[16:20]
        self._shutting_down = self.__fromBitStatus(statusBits, 7)
        self._guard_flame_on = self.__fromBitStatus(statusBits, 8)
        self._igniting = self.__fromBitStatus(statusBits, 11)
        self._aux_on = self.__fromBitStatus(statusBits, 12)
        self._light_on = self.__fromBitStatus(statusBits, 13)

        # Convert the range 100 -> 251 to 0 -> 255
        self._light_brightness = round(((int("0x" + statusStr[20:22], 0) - 100) / 151) * 255)
        
        if self._light_brightness < 0 or not self._light_on:
            self._light_brightness = 0

        self._ambient_temperature = int("0x" + statusStr[30:32], 0) / 10

        # print("Status update!!")
        # print("Fireplace on: " + str(self.on))
        # print("Flame height: " + str(flameHeight))
        # print("Guard flame on: " + str(guardFlameOn))
        # print("Igniting: " + str(igniting))
        # print("Shutting down: " + str(shuttingDown))
        # print("Aux on: " + str(self.auxOn))
        # print("Light on: " + str(self._light_on))
        # print("Dim level: " + str(self._dim_level))
        #        console.log("Ambient temp: " + ambientTemp)

        # opMode = "on"


""""
        if self.on == False and igniting == False:
            if guardFlameOn and shuttingDown == False:
                opMode = "stand_by"
            else:
                opMode = "off"
        else:
            if mode == "2":
                self.offToEco = False
                opMode = "eco"
            else:
                if self.offToEco:
                    self.setEco()
                    opMode = "eco"

        print("Fire control mode: " + mode)
        print("Operation mode: " + opMode)
"""

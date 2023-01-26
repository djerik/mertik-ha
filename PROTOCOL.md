# Protocol documentation

Every package starts with `02` (*STX: Start of text*) followed by the prefix, a command, the payload and ends with `03` (*ETX: End of Text*).

```
02 [PREFIX] [COMMAND] [PAYLOAD] 03
```

| Prefix | HEX | Description |
|---|---|---|
| Request | `33 30 33 30 33 30 33 30 38 30` | Use this prefix to send data to the WiFi-module |
| Response | `30 33 30 33 30 30 30 30 30 30` | This prefix will be used when receiving a response for the request |

> TODO:
> - Figure out how the prefix works

| Command | HEX | Description |
|---|---|---|
| [Date and time](#date-and-time) | `30 36` | Set or get the date and time |
| [Light](#light) | `33 30` | Turn the light on, off or set its brightness |
| [Settings](#settings) | `44 31` | Configure the settings |

# Payloads

## Date and time

### Request

```
[ACTION] [DATE TIME: xx xx xx xx xx xx xx xx xx xx xx xx xx xx]
```

### Response

```
[DATE TIME: xx xx xx xx xx xx xx xx xx xx xx xx xx xx]
```

### Values

| Action | HEX | Description |
|---|---|---|
| Set | `46 45` | Set the date and time |
| Get | `46 46` | Get the date and time |

| Date time | HEX | Description |
|---|---|---|
| Year | `xx xx` | The year<br />*Without the leading two digits* |
| Month | `xx xx` | The month |
| Day | `xx xx` | The day of the month |
| Weekday | `xx xx` | The day of the week<br />*Ranges from 1 (Monday) to 7 (Sunday)* |
| Hour | `xx xx` | The hour |
| Minute | `xx xx` | The minute |
| Second | `xx xx` | The second |

Each decimal value is encoded to the `xx xx` value by first encoding it to ASCII and then to HEX. Decoding is the other way around. Below you can see en example how the date time `2023-01-21 22:14:47` is encoded/decoded.

| | Year | Month | Day | Weekday | Hour | Minute | Second |
|---|---|---|---|---|---|---|---|
| Decimal | `23` | `1` | `21` | `6` | `22` | `14` | `47` |
| ASCII | `17` | `01` | `15` | `06` | `16` | `0E` | `2F` |
| HEX | `31 37` | `30 31` | `31 35` | `30 36` | `31 36` | `30 45` | `32 46` |

## Light

### Request

```
[ACTION] [BRIGHTNESS (optional)]
```

### Response

```
[STATUS] [BRIGHTNESS]
```

### Values

| Action | HEX | Description |
|---|---|---|
| Off | `30 30` | Turn the light off |
| On | `30 31` | Turn the light on |
| Set | `46 45` | Set the brightness |

| Brightness | HEX | Description |
|---|---|---|
| Off | `30 30` | Turn the light off using the set action |
| Value | `xx xx` | The brightness of the light (between `36 33` and `46 42`) |

| Status | HEX | Description |
|---|---|---|
| Off | `30 30` | The light is off |
| On | `30 31` | The light is on |

> TODO:
> - Check min/max range
> - Figure out how the HEX values are calculated

## Settings

### Request

```
[SETTING: xx xx] [xx] [FEATURES: xx xx] [xx xx xx xx] 30 30 30 30
```

### Response

```
[SETTING: xx xx] [???: xx] [FEATURES: xx xx] [xx xx xx xx]
```

### Values

| Setting | HEX | Description |
|---|---|---|
| Icon | `30 30` | Oven icon |
| | `30 31` | Single bed icon |
| | `30 32` | Double bed icon |
| | `30 33` | Chair icon |
| | `30 34` | Couch icon |
| Fireplace name | `46 46` | The name of the fireplace |

| Features | HEX | Bitmask | Description |
|---|---|---|---|
| Timer | `xx 3x` | `???? ???? 0011 ????` | [...] |
| Fan | `xx 3x` | `???? ???? 0011 0001` | [...] |
| Light | `xx 3x` | `???? ???? 0011 0010` | [...] |
| Aux | `xx 3x` | `???? ???? 0011 0100` | [...] |

> TODO:
> - Add bitmask explanation

| ??? | HEX | Description |
|---|---|---|
| [...] | `xx` | [...] |

# Todo
- Add more commands
  - Set fireplace to on/off/eco/manual
  - Turn aux burner on/off
  - Get/set flame height
  - Get ambient temperature
  - Get status
  - [...]

# Changelog
- 2023-01-21 Initial version

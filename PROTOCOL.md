# Protocol description

Every package starts with `02` (*STX: Start of text*) followed by the identifier, a command, the payload and ends with `03` (*ETX: End of Text*).

```
02 [IDENTIFIER] [COMMAND] [PAYLOAD] 03
```

| Identifier | HEX | Description |
|---|---|---|
| Request | `33 30 33 30 33 30 33 30 38 30` | Use this identifier to send data to the WiFi-module |
| Response | `30 33 30 33 30 30 30 30 30 30` | This identifier will be used when receiving a response for the request |

> TODO:
> - Figure out how the HEX values are calculated

| Command | HEX | Description |
|---|---|---|
| [Date and time](#date-and-time) | `30 36` | Set or get the date and time |
| [Light](#light) | `33 30` | Turn the light on, off or set its brightness |
| [Settings](#settings) | `44 31` | Configure the settings |

# Payloads

## Date and time

### Request

```
30 36 [ACTION] [DATE TIME: YYYY mm dd HH MM SS]
```

### Response

```
30 36 [DATE TIME: YYYY mm dd HH MM SS]
```

### Values

| Action | HEX | Description |
|---|---|---|
| Set | `46 45` | Set the date and time |
| Get | `46 46` | Get the date and time |

| Date time | HEX | Description |
|---|---|---|
| Year | `xx xx xx xx` | [...] |
| Month | `xx xx` | [...] |
| Day | `xx xx` | [...] |
| Hour | `xx xx` | [...] |
| Minute | `xx xx` | [...] |
| Second | `xx xx` | [...] |

> TODO:
> - Figure out how the HEX values are calculated

## Light

### Request

```
33 30 [ACTION] [BRIGHTNESS (optional)]
```

### Response

```
33 30 [STATUS] [BRIGHTNESS]
```

### Values

| Action | HEX | Description |
|---|---|---|
| Off | `30 30` | Turn the light off |
| On | `30 31` | Turn the light on |
| Set | `46 45` | Set the brightness |

| Status | HEX | Description |
|---|---|---|
| Off | `30 30` | The light is off |
| On | `30 31` | The light is on |

| Brightness | HEX | Description |
|---|---|---|
| Off | `30 30` | Turn the light off using the set action |
| Value | `xx xx` | The brightness of the light (between `36 33` and `46 42`) |

> TODO:
> - Check min/max range
> - Figure out how the HEX values are calculated

## Settings

### Request

```
44 31 [IDENTIFICATION: xx xx] [xx] [FEATURES: xx xx] [xx xx xx xx] 30 30 30 30
```

### Response

```
44 31 [IDENTIFICATION: xx xx] [xx] [FEATURES: xx xx] [xx xx xx xx]
```

### Values

| Identification | HEX | Description |
|---|---|---|
| Icon | `30 30` | Oven icon |
| | `30 31` | Single bed icon |
| | `30 32` | Double bed icon |
| | `30 33` | Chair icon |
| | `30 34` | Couch icon |
| Fireplace name | `46 46` | The name of the fireplace |

| [...] | HEX | Description |
|---|---|---|
| [...] | `xx` | [...] |

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
| [...] | `xx xx xx xx` | [...] |

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

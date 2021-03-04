---
sort: 2
---

# Configuration

Configuration of the desired client behaviors, network conditions, VPN access, and so on are specified in the `config.json` file in the root directory of this tool.

| Key        | Description                                                                                                                                                                             |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| behaviors  | List of one or more target behaviors. All target behaviors will be run for each specified set of network conditions. For possible values see [Behaviors](#behaviors).     |
| conditions | List of nested configuration specifying desired network conditions. E.g. `[{"latency": "50ms", "bandwidth": "10Mbps"}]`. For configuration see [Conditions](#conditions). |
| vpn        | Nested configuration for a VPN connection. For configuration see [VPN Config](#vpn).                                                                                             |

## Behaviors

List of values. Possible values:

| Value     | Description                                                               |
| --------- | ------------------------------------------------------------------------- |
| `none`      | Do nothing.                                                               |
| `ping`      | Ping a DNS server once every three seconds. Great for testing purposes.                               |
| `browsing`  | Run a script to endlessly browse Twitter.                                 |
| `streaming` | Run a script to endlessly watch YouTube.                                  |
| `custom/<filename.py>` | Run a custom Python script. See [Using Custom Scripts](3_extending.md).

## Conditions

List of nested objects. Each object has keys:

| Key       | Description                                                                       |
| --------- | --------------------------------------------------------------------------------- |
| latency   | Milliseconds. The desired amount of network latency to be injected. E.g. `"50ms"` |
| bandwidth | Megabits per second. The desired download speed. E.g. `"10Mbit"`                  |

## VPN

Nested object. Keys:

| Key     | Description                                                          |
| ------- | -------------------------------------------------------------------- |
| enabled | `true` or `false`. Whether or not a VPN should be used. |
| server  | URL or IP to the desired VPN service. E.g. `"vpn.ucsd.edu"`. |
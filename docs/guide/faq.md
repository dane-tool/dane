---
sort: 6
---

# Frequently Asked Questions

- [The tool isn't working. It fails silently, or fails to launch behaviors or network-stats.](#the-tool-isnt-working-it-fails-silently-or-fails-to-launch-behaviors-or-network-stats)
- [VPN - "User input required in non-interactive mode Failed to obtain WebVPN cookie"](#vpn---user-input-required-in-non-interactive-mode-failed-to-obtain-webvpn-cookie)
- [Speedtest - "Cannot open socket: Timeout occurred in connect."](#speedtest---cannot-open-socket-timeout-occurred-in-connect)
- [I have a question that's not on this list](#i-have-a-question-thats-not-on-this-list)


## The tool isn't working. It fails silently, or fails to launch behaviors or network-stats.

Make sure that all submodules have been cloned. You can do this by running
```bash
git submodule update --init --recursive
```

## VPN - "User input required in non-interactive mode Failed to obtain WebVPN cookie"

This shows up after an `Exception: dane_client-... did not connect to the VPN!` and is due to an empty or misconfigured .env file, or if you didn't authorize a 2-Factor Authentication in time. If you're connecting to a VPN, [Getting Started - Environment files](quickstart.md#environment-file-secrets) may help you set up the file.

## Speedtest - "Cannot open socket: Timeout occurred in connect."

This shows up after an `Exception: Exception: Speedtest failed in dane_client-...` and happens when the Ookla speed test times out. It might be because your configured network conditions are reaaaaally poor, or it might just be bad luck. Often times waiting a moment then trying again works!

## I have a question that's not on this list

Great! Feel free to [post an Issue](https://github.com/dane-tool/dane/issues/new) or [start a Discussion](https://github.com/dane-tool/dane/discussions/new) at our [GitHub repository](https://github.com/dane-tool/) and we'd be happy to assist you -- and maybe even add your question to this list.

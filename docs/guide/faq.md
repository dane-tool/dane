---
sort: 6
---

# Frequently Asked Questions

- [The tool isn't working. It fails silently, or fails to launch behaviors or network-stats.](#the-tool-isnt-working-it-fails-silently-or-fails-to-launch-behaviors-or-network-stats)
- ["User input required in non-interactive mode Failed to obtain WebVPN cookie"](#user-input-required-in-non-interactive-mode-failed-to-obtain-webvpn-cookie)
- [I have a question that's not on this list](#i-have-a-question-thats-not-on-this-list)


## The tool isn't working. It fails silently, or fails to launch behaviors or network-stats.

Make sure that all submodules have been cloned. You can do this by running
```bash
git submodule update --init --recursive
```

## "User input required in non-interactive mode Failed to obtain WebVPN cookie"

This shows up after an `Exception: dane_client-... did not connect to the VPN!` and is due to an empty or misconfigured .env file. If you're connecting to a VPN, [Getting Started - Environment files](quickstart.md#environment-file-secrets) may help you set up the file.

## I have a question that's not on this list

Great! Feel free to [post an Issue](https://github.com/dane-tool/dane/issues/new) or [start a Discussion](https://github.com/dane-tool/dane/discussions/new) at our [GitHub repository](https://github.com/dane-tool/) and we'd be happy to assist you -- and maybe even add your question to this list.

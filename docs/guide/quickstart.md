---
sort: 1
---

# Tool Quickstart

To use the tool, you must configure your desired network conditions and behaviors.

Source code for the tool can be found at [network-data-generation](https://github.com/dane-tool/dane).

## Requirements

The data collcetion tool runs on Linux. You will need:

- [Docker 19.03+](https://docs.docker.com/get-docker/)
- [Docker Compose 1.27+](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)

## Getting Started

You can start using this tool and conducting analysis of different network conditions by running:

```bash
git clone \
https://github.com/dane-tool/dane.git \
--recursive
```

## Environment file and secrets

The containers will need secret variables that store things like VPN or website login credentials.

Please create a file named `.env` and place it in this directory. Inside the file, add the login information for your VPN:

```
VPN_USERNAME=<your username>
VPN_USERGROUP=<the 'group' to use for the VPN -- probably "2-Step Secured - allthruucsd">
VPN_PASSWORD=<your password>
```

## Running

Once you're satisfied with your configuration, simply open a terminal to this directory, and run

```bash
make
```

When you're done collecting data, open a new terminal in this directory and run

```bash
make stop
```

## Example

![](../media/demo.gif)

## Data

After the tool has been stopped, data can be found in `data/`.

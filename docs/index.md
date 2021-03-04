<link rel="shortcut icon" type="image/png" href="media/favicon.png">
<h1 align="center"><b>DANE - Data Automation and Network Emulation Tool</b> </h1>
<hr>

## Why Use DANE?

DANE provides two core functionalities:

1. Automatically collect network traffic datasets in a parallelized manner

   Manual data collection for network traffic datasets is a long and tedious process—run the tool and you can easily collect multiple hours of data in one hour of time (magic!) with one or many desired 'user' behaviors.

2. Emulate a diverse range of network conditions that are representative of the real world

   Data representation is an increasingly relevant issue in all fields of data science, but generating a dataset while connected to a fixed network doesn't capture diversity in network conditions—in a single file, you can configure DANE to emulate a variety of network conditions, including latency and bandwidth.

You can easily hack the tool to run custom scripts, custom data collection tools, and other custom software dependencies which support your particular research interest.

## Tool

Our tool establishes Docker containers with configurable network conditions,
then runs target behaviors such as browsing the internet, and collects data on
the network traffic generated using
[network-stats](https://github.com/Viasat/network-stats).

To use the tool, you must configure your desired network conditions and behaviors.

Source code for the tool can be found at [network-data-generation](https://github.com/dane-tool/dane).

### Requirements

The data collcetion tool runs on Linux. You will need:

- [Docker 19.03+](https://docs.docker.com/get-docker/)
- [Docker Compose 1.27+](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)

### Getting Started

You can start using this tool and conducting analysis of different network conditions by running:

```bash
git clone \
https://github.com/dane-tool/dane.git \
--recursive
```

### Environment file and secrets

The containers will need secret variables that store things like VPN or website login credentials.

Please create a file named `.env` and place it in this directory. Inside the file, add the login information for your VPN:

```
VPN_USERNAME=<your username>
VPN_USERGROUP=<the 'group' to use for the VPN -- probably "2-Step Secured - allthruucsd">
VPN_PASSWORD=<your password>
```

### Running

Once you're satisfied with your configuration, simply open a terminal to this directory, and run

```bash
make
```

When you're done collecting data, open a new terminal in this directory and run

```bash
make stop
```

### Example

![](media/demo.gif)

### Data

After the tool has been stopped, data can be found in `data/`.

### FAQ

1. The tool isn't working. It fails silently, or fails to launch behaviors or network-stats.
   Make sure that all submodules have been cloned. You can do this by running
   ```bash
   git submodule update --init --recursive
   ```

## Proof of Concept

Check out an example of some work that can be done with DANE!

(TODO - Link to Analysis Report)

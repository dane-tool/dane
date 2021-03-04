---
sort: 4
---

# How It Works

When DANE is run, it utilizes a handful of [Services](#services) (Docker containers and networks) to conduct the various aspects of automated network traffic generation and collection.

For each set of network conditions you've configured, these services are assembled into a specific [Networking Layout](#networking-layout) which enables multiple sets of conditions to run side by side on your computer.

All of these services and layouts are defined from your configuration using a [Configuration Pipeline](#configuration-and-tool-pipeline).

## Services

There are four main types of Docker services that are used while the tool is running. Each service has its own responsibilities, and if it's a container it comes with its own image supporting specific software dependencies.

### Client

'Client' containers act like internet users, they use the Internet and create the raw data like a person would.

<center><img src='../../media/client-icon.png' height=80></center>

#### Responsibilities

- Engage in behavior that produces network traffic -- like browsing the web or watching videos
- Collect the network traffic data by using a tool -- like [network-stats](https://github.com/Viasat/network-stats/) (currently used) or [TShark](https://tshark.dev/)
- Do anything else an end-user might do -- like connecting to a VPN or running background software services

#### Software

Clients have software that enables them to access the internet and use it. Each client generates and collects its own network traffic data in isolation from the other clients. This approach enables a high degree of parallelization in data collection.

- Firefox -- web browser
- Selenium -- web automation, uses the Python API
- Python -- run arbitrary scripts like [network-stats](https://github.com/Viasat/network-stats/) and [starter-scripts](https://github.com/dane-tool/starter-scripts/)
- iproute2 -- connect to the router
- Speedtest -- check achieved network conditions
- OpenConnect -- connect to a VPN

Since the Dockerfile which defines these software dependencies is kept locally, it is very easy to specify additional software to run on the clients.

#### Usage

During a tool run, a client is created for each combination of *behavior* and *condition* specified in your configuration.

---
### Router

'Router' containers act like their physical namesake, they only care about networking.

<center><img src='../../media/router-icon.png' height=80></center>

#### Responsibilities

- Route communications between clients and the Internet
- Configure the network conditions for clients connected to it -- emulate conditions like latency and bandwidth

#### Software

The only software needed for a router is to route packets and emulate conditions.

- iptables -- to route packets between the internal network and the Internet
- iproute2 -- includes `tc` (traffic controller) to emulate conditions

#### Usage

During a tool run, a router is created for each *condition* specified in your configuration.

---
### Network

DANE utilizes Docker-created networks to serve as the connection between clients and routers. This allows for multiple different network conditions to be present on a single local machine (the "host") while still remaining isolated from each other and not affecting the host's network connection.

<center><img src='../../media/network-icon.png' height=80></center>

As networks are not containers, they do not have any software or responsibilities -- other than to just exist!

#### Usage

During a tool run, a network is created for each *condition* specified in your configuration.

---
### Daemon

The 'daemon' container acts as a manager to all other containers. The daemon tells all other containers when to run their commands and scripts, and is therefore at the core of the automation capabilities of this tool.

<center><img src='../../media/daemon-icon.png' height=80></center>

#### Responsibilities

- Instruct routers to set up conditions based on configuration
- Instruct clients to run behaviors scripts based on configuration, and to run collection scripts
- Instruct clients to run additional commands like VPN connections or additional software
- Interrupt and tear down all containers when tool use is finished

#### Software

The daemon doesn't do much on its own, but it needs to be able to manage other Docker containers.

- Docker
- Python -- uses the Docker API and runs the management script

#### Usage

During a tool run, a single daemon is created.

## Networking Layout

**(WIP)**

![](../media/network-layout.svg)

## Configuration and Tool Pipeline

**(WIP)**

![](../../docs/media/config-pipeline.svg)

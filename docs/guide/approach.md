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

Clients have software that enables them to access the internet and use it.

- Firefox -- web browser
- Selenium -- web automation, uses the Python API
- Python -- run arbitrary scripts like [network-stats](https://github.com/Viasat/network-stats/) and [starter-scripts](https://github.com/dane-tool/starter-scripts/)
- iproute2 -- connect to the router
- Speedtest -- check achieved network conditions
- OpenConnect -- connect to a VPN

Since the Dockerfile which defines these software dependencies is kept locally, it is very easy to specify additional software to run on the clients.

#### Usage

During a tool run, a client is created for each combination of *behavior* and *condition* specified in your configuration.

Each client generates and collects its own network traffic data in isolation from the other clients. This approach enables a high degree of parallelization in data collection.

**(WIP)**

- three services -- client (user-like behavior), router (network conditions), daemon (manager)
- networking setup
- configuration setup


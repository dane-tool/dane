---
sort: 1
---

# Why Use DANE?

DANE provides two core functionalities:

1. Automatically collect network traffic datasets in a parallelized manner

   Manual data collection for network traffic datasets is a long and tedious process—run the tool and you can easily collect multiple hours of data in one hour of time (magic!) with one or many desired 'user' behaviors.

2. Emulate a diverse range of network conditions that are representative of the real world

   Data representation is an increasingly relevant issue in all fields of data science, but generating a dataset while connected to a fixed network doesn't capture diversity in network conditions—in a single file, you can configure DANE to emulate a variety of network conditions, including latency and bandwidth.

By default DANE utilizes a VPN connection and collects data using [network-stats](https://github.com/Viasat/network-stats/), but these choices are modifiable. You can easily hack the tool to run custom scripts, custom data collection tools, and other custom software dependencies which support your particular research interest.

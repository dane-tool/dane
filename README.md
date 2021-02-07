# network-data-generation

Generate network communication data for target tasks in diverse network conditions.

**Table of contents**
- [What does it do](#what-does-it-do)
- [How to use](#how-to-use)
- [Approach](#approach)
- [Requirements](#requirements)
- [Example](#example)
- [Software / References](#software--references)

**Note:** This is currently being developed primarily on **Windows 10** and **Linux**. If you are on Windows 10 you *must* use the **Hyper-V backend** for Docker. The WSL2 backend doesn't seem to work. This runs on Linux by using a docker-compose override which is added automatically. Mac is a mystery at the moment since my old Mac is incapable of running Docker (!), but theoretically Mac should work the same as Windows.

## What does it do

TODO

## How to use

1. Clone this repository with the submodule
   ```
   git clone --recurse-submodules
   ```
   then navigate to this directory.

2. Build the Docker images
   ```
   make build
   ```

3. Specify target conditions and behaviors

   TODO. Modify the `docker/docker-compose.yml` file.

4. Add secret configuration

   Any usernames and passwords should be added to a `.env` file in the root directory of this project. At the moment these environment variables are used solely for logging in to the UCSD VPN.
   ```
   # In the .env file:
   VPN_USERNAME=<your UCSD username>
   VPN_USERGROUP=<the 'group' to use for the VPN -- probably "2-Step Secured - allthruucsd">
   VPN_PASSWORD=<your UCSD password>
   ```

5. Run the tool, deploying all containers specified in the Compose file
   ```
   make run
   ```

6. Interrupt the tool
   
   To gracefully stop this tool, you must send an interrupt signal to the daemon. You can send this from a new terminal window or tab. Failure to send the interrupt will result in the data for that session not being collected.
   ```
   make interrupt
   ```

   The daemon will catch the interrupt and tear down all containers. Collected data will be present in `data/`.

7. Finish with the tool completely
   
   Once you are completely done with the tool, you can ensure all aspects of the tool are stopped.
   ```
   make stop
   ```
   And you can remove the built Docker images from your machine with
   ```
   make clean
   ```
   (you will need to rebuild the images if you choose to run this)

## Approach

1. Clients and Daemon are launched with a `docker-compose.yml`
   - Clients have labels to specify their target behavior and network conditions
   - In the future, this file should be programmatically generated from configuration files to specify all desired behaviors and conditions (generating programmatically will also help with OS support)
2. Daemon is in charge of executing all commands on the Clients.
   1. Launches Controller container which attaches to the network of a Client and emulates conditions based on the labels
   2. Executes target behavior script on Client based on label
   3. Executes network-stats on Client using labels in the naming convention
   4. Enforces time limit, interrupts and tears down application
3. Network-stats output are saved to a data directory

## Requirements

This project runs on Linux, Mac, and Windows Pro or Education (Hyper-V must be available).

You will need [**Docker 19.03+**](https://docs.docker.com/get-docker/) and [**Docker Compose 1.27+**](https://docs.docker.com/compose/install/) (on Windows and Mac this is included with your installation of Docker Desktop) in order to run.

Finally, [**GNU Make**](https://www.gnu.org/software/make/) is used to make running specific tasks easier (by just running `make <target>` rather than running a `docker` or `docker-compose` command directly). If you're on Windows I recommend using **GitBash** as your main terminal, and referencing [this link](https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows) for installing make. If you're on Mac you can use homebrew to `brew install make`.

## Example

```bash
make build # Set up images
make run # Run the containerized network emulation
```

![](docs/media/demo.gif)

## Software / References

- [netem]: https://wiki.linuxfoundation.org/networking/netem
  [**TC NetEm documentation**][netem]. Used to emulate network conditions.
- [compose]: https://github.com/compose-spec/compose-spec/blob/master/spec.md
  [**Docker Compose YAML specification**][compose]. Used to handle options when launching multiple docker containers (clients and daemon).

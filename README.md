# network-data-generation

Generate network communication data for target tasks in diverse network conditions.

**Table of contents**
- [Approach](#approach)
- [Example](#example)
- [Software / References](#software--references)

**Note:** This is currently being developed primarily on **Windows 10**. If you are on Windows 10 you *must* use the **Hyper-V backend** for Docker. The WSL2 backend doesn't seem to work. This runs on Linux with some modifications to how the daemon is mounted (needs /var/run/docker.sock) -- rename `docker-compose.linux.yml` to `docker-compose.yml`. Mac is a mystery at the moment, but theoretically should work the same as Windows.

## Approach

1. Clients and Daemon are launched with a `docker-compose.yml`
   - Clients have labels to specify their target behavior and network conditions
   - In the future, this file should be programatically generated from configuration files to specify all desired behaviors and conditions (generating programatically will also help with OS support)
2. Daemon is in charge of executing all commands on the Clients.
   1. Launches Controller container which attaches to the network of a Client and emulates conditions based on the labels
   2. Executes target behavior script on Client based on label
   3. Executes network-stats on Client using labels in the naming convention
   4. Enforces time limit, interrupts and tears down application
3. Network-stats output are saved to a data directory

## Example

```bash
make build # Set up images
make run # Run the containerized network emulation
```

![](docs/media/demo.gif)

## Software / References

- [netem]: https://wiki.linuxfoundation.org/networking/netem
  [**TC NetEm**][netem] documentation. Used to emulate network conditions.
- [compose]: https://github.com/compose-spec/compose-spec/blob/master/spec.md
  [**Docker Compose**][compose] specification for docker-compose.yml files. Used to handle options when launching multiple docker containers (clients and daemon).

---
sort: 4
---

# Using Local Images

If you would like to modify the Docker images used by the Client, Router, or Daemon to install custom dependencies or run custom software, you can do so.

Simply modify the respective Dockerfile found at `docker/<service_name>/Dockerfile` then run:
```bash
make build
```

This may take a few minutes.

Finally, modify your configuration to use these locally built images. See [Configuration - System](config.md#system).

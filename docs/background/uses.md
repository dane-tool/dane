---
sort: 2
---

# Example Use Cases

- Analyzing network traffic in diverse network conditions ([pdf]())
  - We've collected 50+ hours of streaming and browsing network traffic under a VPN to test an encrypted traffic classification model under multiple network conditions
- Testing web application performance in different network conditions using Selenium screen captures
  - DANE can set up containers with your [desired network conditions](../guide/config.md)
  - A [custom script](../guide/extending.md) can load the application and take screenshots to help understand performance
- Un-encrypted network traffic research using packet captures
  - You can configure to use a VPN -- or not!
  - You can use a different network monitoring tool, like [TShark](https://tshark.dev/) to collect full packet captures by modifying the client's Dockerfile and collection.py script

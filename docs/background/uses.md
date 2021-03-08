---
sort: 2
---

# Example Use Cases

- Analyzing network traffic in diverse network conditions ([pdf](../media/Analyzing-Network-Traffic-In-Diverse-Network-Conditions.pdf))
  - We've collected 50+ hours of streaming and browsing network traffic under a VPN to test an encrypted traffic classification model under multiple network conditions
- Testing web application performance in different network conditions using Selenium screen captures
  - DANE can set up containers with your [desired network conditions](../guide/config.md)
  - A [custom script](../guide/custom-scripts.md) can load the application and take screenshots to help understand performance
- Un-encrypted network traffic research using packet captures
  - You can configure to use a VPN -- or not!
  - You can use a different network monitoring tool, like [TShark](https://tshark.dev/) to collect full packet captures by modifying the client's Dockerfile and collection.py script
- Collect data that resembles real-world client data
  - By modifying the client Dockerfile, you can have the container run background services that add realistic noise to your network data
- See what different network conditions look like first hand
  - If you really want to hack the tool, you can connect a VNC to the client containers to run their browser windows as a GUI application!

# network-data-generation

Generate network communication data for target tasks in diverse network conditions.

**Note:** This is currently being developed on **Windows 10**. If you are on Windows 10 you *must* use the **Hyper-V backend** for Docker. WSL2 will not work.

## Example

```bash
make build
make start

# In a new terminal window
make delay
```

You should see that the ping for client_1 is 300ms greater than the others.

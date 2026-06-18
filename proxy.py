from fastmcp.server import create_proxy

mcp = create_proxy(
    "https://expense-remote-server-30.fastmcp.app/mcp"
)

if __name__ == "__main__":
    mcp.run()
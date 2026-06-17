from fastmcp import FastMCP
import random
import json

mcp = FastMCP("Simple Calculator Server")


@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """
    Add two numbers together.

    Args:
        a: The first number
        b: The second number

    Returns:
        The sum of a and b
    """
    return a + b


@mcp.tool()
def random_numbers(min_val: int = 1, max_val: int = 100) -> int:
    """
    Generate a random number between min_val and max_val.

    Args:
        min_val: The minimum value
        max_val: The maximum value

    Returns:
        A random integer
    """
    return random.randint(min_val, max_val)

@mcp.resource("info://server")
def server_info() ->str:
    """Get information about the server"""
    info = {
        "name": "Simple Calculator Server",
        "version": "1.0.0",
        "description": "A basic MCP server with math tools",
        "tools": ["add", "random_numbers"],
        "author":"Utkarsh Patil"
    }
    return json.dumps(info, indent=2)

if __name__=="__main__":
    mcp.run(transport="http",host="0.0.0.0",port=8000)
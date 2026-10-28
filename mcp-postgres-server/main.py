import os
from mcp.server.fastmcp import FastMCP
from tools import list_schemas, describe_table, query

# Initialize MCP server
mcp = FastMCP("mcp-postgres-server")

# Register tools
mcp.tool()(list_schemas)
mcp.tool()(describe_table)
mcp.tool()(query)

if __name__ == "__main__":
    mcp.run()

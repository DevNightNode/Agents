import os
from dotenv import load_dotenv
from tools import mcp

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Validate required environment variable
    project_dir = os.getenv("PROJECT_DIR")
    if not project_dir:
        raise ValueError("PROJECT_DIR environment variable is required")
    
    # Verify project directory exists
    if not os.path.exists(project_dir):
        raise ValueError(f"PROJECT_DIR '{project_dir}' does not exist")
    
    # Run the MCP server
    mcp.run()

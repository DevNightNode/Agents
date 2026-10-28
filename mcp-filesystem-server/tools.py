import os
import re
from pathlib import Path
from typing import List, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("filesystem-server")

@mcp.tool()
def read_file(file_path: str) -> str:
    """
    Read the contents of a file.
    
    Args:
        file_path (str): The path to the file to read
        
    Returns:
        str: The contents of the file
        
    Raises:
        FileNotFoundError: If the file does not exist
        PermissionError: If the file cannot be read due to permissions
    """
    try:
        # Resolve the path relative to the project directory
        project_dir = os.getenv("PROJECT_DIR", ".")
        full_path = os.path.join(project_dir, file_path)
        
        # Security check: prevent directory traversal
        if not os.path.abspath(full_path).startswith(os.path.abspath(project_dir)):
            raise PermissionError("Access denied: Path traversal attempt")
            
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to read file {file_path}: {str(e)}")

@mcp.tool()
def write_file(file_path: str, content: str) -> str:
    """
    Write content to a file.
    
    Args:
        file_path (str): The path to the file to write
        content (str): The content to write to the file
        
    Returns:
        str: Success message
        
    Raises:
        PermissionError: If the file cannot be written due to permissions
        OSError: If there's an OS-level error
    """
    try:
        # Resolve the path relative to the project directory
        project_dir = os.getenv("PROJECT_DIR", ".")
        full_path = os.path.join(project_dir, file_path)
        
        # Security check: prevent directory traversal
        if not os.path.abspath(full_path).startswith(os.path.abspath(project_dir)):
            raise PermissionError("Access denied: Path traversal attempt")
            
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        raise RuntimeError(f"Failed to write to file {file_path}: {str(e)}")

@mcp.tool()
def list_directory(directory_path: str = ".") -> List[str]:
    """
    List files and directories in a directory.
    
    Args:
        directory_path (str): The path to the directory to list (default: current directory)
        
    Returns:
        List[str]: List of file and directory names
        
    Raises:
        FileNotFoundError: If the directory does not exist
        PermissionError: If the directory cannot be accessed due to permissions
    """
    try:
        # Resolve the path relative to the project directory
        project_dir = os.getenv("PROJECT_DIR", ".")
        full_path = os.path.join(project_dir, directory_path)
        
        # Security check: prevent directory traversal
        if not os.path.abspath(full_path).startswith(os.path.abspath(project_dir)):
            raise PermissionError("Access denied: Path traversal attempt")
            
        items = os.listdir(full_path)
        return items
    except Exception as e:
        raise RuntimeError(f"Failed to list directory {directory_path}: {str(e)}")

@mcp.tool()
def search_files(pattern: str, directory_path: str = ".") -> List[str]:
    """
    Search for files matching a pattern in a directory.
    
    Args:
        pattern (str): The regex pattern to match file names
        directory_path (str): The directory to search in (default: current directory)
        
    Returns:
        List[str]: List of matching file paths
        
    Raises:
        re.error: If the regex pattern is invalid
        PermissionError: If the directory cannot be accessed due to permissions
    """
    try:
        # Resolve the path relative to the project directory
        project_dir = os.getenv("PROJECT_DIR", ".")
        full_path = os.path.join(project_dir, directory_path)
        
        # Security check: prevent directory traversal
        if not os.path.abspath(full_path).startswith(os.path.abspath(project_dir)):
            raise PermissionError("Access denied: Path traversal attempt")
            
        compiled_pattern = re.compile(pattern)
        matches = []
        
        for root, dirs, files in os.walk(full_path):
            for file in files:
                if compiled_pattern.search(file):
                    # Return relative path from project directory
                    rel_path = os.path.relpath(os.path.join(root, file), project_dir)
                    matches.append(rel_path)
        
        return matches
    except Exception as e:
        raise RuntimeError(f"Failed to search files: {str(e)}")

@mcp.tool()
def move_file(source_path: str, destination_path: str) -> str:
    """
    Move a file from source to destination.
    
    Args:
        source_path (str): The path to the source file
        destination_path (str): The path to the destination file
        
    Returns:
        str: Success message
        
    Raises:
        FileNotFoundError: If the source file does not exist
        PermissionError: If the file cannot be moved due to permissions
        OSError: If there's an OS-level error
    """
    try:
        # Resolve the paths relative to the project directory
        project_dir = os.getenv("PROJECT_DIR", ".")
        source_full_path = os.path.join(project_dir, source_path)
        dest_full_path = os.path.join(project_dir, destination_path)
        
        # Security check: prevent directory traversal
        if not os.path.abspath(source_full_path).startswith(os.path.abspath(project_dir)):
            raise PermissionError("Access denied: Path traversal attempt in source")
        if not os.path.abspath(dest_full_path).startswith(os.path.abspath(project_dir)):
            raise PermissionError("Access denied: Path traversal attempt in destination")
            
        # Create destination directory if it doesn't exist
        os.makedirs(os.path.dirname(dest_full_path), exist_ok=True)
        
        # Move the file
        os.rename(source_full_path, dest_full_path)
        
        return f"Successfully moved {source_path} to {destination_path}"
    except Exception as e:
        raise RuntimeError(f"Failed to move file from {source_path} to {destination_path}: {str(e)}")

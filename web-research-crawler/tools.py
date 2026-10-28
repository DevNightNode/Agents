import os
import requests
from bs4 import BeautifulSoup
from crewai.tools import tool
import markdown
from urllib.parse import urljoin, urlparse
import time
from typing import List, Dict, Any

@tool("Web Search")
def web_search(query: str) -> str:
    """
    Search the web for information related to the query.
    
    Args:
        query (str): The search query string
        
    Returns:
        str: Search results formatted as markdown
    """
    # Using a simple web search approach with DuckDuckGo
    search_url = "https://html.duckduckgo.com/html/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(search_url, params={"q": query}, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        for result in soup.find_all('div', class_='result'):
            title_elem = result.find('a', class_='result__a')
            snippet_elem = result.find('a', class_='result__snippet')
            
            if title_elem and snippet_elem:
                title = title_elem.get_text(strip=True)
                snippet = snippet_elem.get_text(strip=True)
                url = title_elem.get('href', '')
                
                results.append(f"**[{title}]({url})**\n{snippet}\n")
        
        return "\n".join(results) if results else "No results found."
        
    except Exception as e:
        return f"Search failed: {str(e)}"

@tool("Fetch URL")
def fetch_url(url: str) -> str:
    """
    Fetch and clean content from a URL.
    
    Args:
        url (str): The URL to fetch content from
        
    Returns:
        str: Cleaned content from the URL
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean it
        text = soup.get_text()
        
        # Break into lines and remove leading/trailing space
        lines = (line.strip() for line in text.splitlines())
        
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Limit to 5000 characters to avoid overly long content
        if len(text) > 5000:
            text = text[:5000] + "..."
            
        return text
        
    except Exception as e:
        return f"Failed to fetch {url}: {str(e)}"

@tool("Write Report")
def write_report(topic: str, content: str, sources: List[Dict[str, str]]) -> str:
    """
    Write a cited markdown report to disk.
    
    Args:
        topic (str): The research topic
        content (str): The main content of the report
        sources (List[Dict[str, str]]): List of source dictionaries with 'url' and 'title' keys
        
    Returns:
        str: Path to the written report file
    """
    try:
        # Create report directory if it doesn't exist
        os.makedirs("reports", exist_ok=True)
        
        # Generate filename from topic
        filename = "".join(c for c in topic.lower() if c.isalnum() or c == ' ').strip().replace(' ', '_')
        filename = f"reports/{filename}.md"
        
        # Create markdown content
        markdown_content = f"# Research Report: {topic}\n\n"
        markdown_content += f"{content}\n\n"
        
        if sources:
            markdown_content += "## Sources\n\n"
            for i, source in enumerate(sources, 1):
                markdown_content += f"{i}. [{source['title']}]({source['url']})\n"
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return f"Report written to {filename}"
        
    except Exception as e:
        return f"Failed to write report: {str(e)}"

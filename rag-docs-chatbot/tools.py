import os
import shutil
from typing import Dict, List
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Global variables to store the vector store and index
vector_store = None
index_path = "chroma_index"

def ingest_directory(directory_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> Dict[str, str]:
    """
    Ingests all text files from a directory into a vector store for semantic search.
    
    Args:
        directory_path (str): Path to the directory containing documentation files
        chunk_size (int): Maximum number of characters per chunk
        chunk_overlap (int): Number of characters to overlap between chunks
    
    Returns:
        Dict[str, str]: Status message about the ingestion process
    """
    global vector_store
    
    # Validate directory exists
    if not os.path.exists(directory_path):
        return {"status": "error", "message": f"Directory {directory_path} does not exist"}
    
    try:
        # Initialize the embedding model
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        # Load documents from directory
        loader = DirectoryLoader(directory_path, loader_cls=TextLoader, recursive=True)
        documents = loader.load()
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        docs = text_splitter.split_documents(documents)
        
        # Create vector store
        vector_store = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=index_path
        )
        
        return {
            "status": "success", 
            "message": f"Ingested {len(documents)} documents from {directory_path} into vector store"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"Failed to ingest directory: {str(e)}"}

def query_index(query: str, k: int = 5) -> Dict[str, List[Dict[str, str]]]:
    """
    Queries the vector store for relevant documents based on a natural language query.
    
    Args:
        query (str): Natural language question to search for
        k (int): Number of relevant documents to return
    
    Returns:
        Dict[str, List[Dict[str, str]]]: List of relevant documents with their content and metadata
    """
    if vector_store is None:
        return {"results": [{"error": "Vector store not initialized. Please ingest a directory first."}]}
    
    try:
        # Perform similarity search
        docs = vector_store.similarity_search(query, k=k)
        
        # Format results
        results = []
        for doc in docs:
            results.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })
        
        return {"results": results}
        
    except Exception as e:
        return {"results": [{"error": f"Failed to query index: {str(e)}"}]}

def refresh_index(directory_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> Dict[str, str]:
    """
    Refreshes the vector store by re-ingesting all text files from a directory.
    
    Args:
        directory_path (str): Path to the directory containing documentation files
        chunk_size (int): Maximum number of characters per chunk
        chunk_overlap (int): Number of characters to overlap between chunks
    
    Returns:
        Dict[str, str]: Status message about the refresh process
    """
    try:
        # Clear existing vector store
        if os.path.exists(index_path):
            shutil.rmtree(index_path)
        
        # Re-ingest directory
        result = ingest_directory(directory_path, chunk_size, chunk_overlap)
        return result
        
    except Exception as e:
        return {"status": "error", "message": f"Failed to refresh index: {str(e)}"}

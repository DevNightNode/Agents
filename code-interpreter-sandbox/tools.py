import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from langchain_core.tools import tool
from typing import List, Dict, Any
import io
import base64

@tool
def load_csv(file_path: str) -> Dict[str, Any]:
    """
    Load a CSV file and return its metadata and first few rows.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        Dict containing file info, columns, and sample data
    """
    try:
        df = pd.read_csv(file_path)
        return {
            "file_path": file_path,
            "shape": df.shape,
            "columns": list(df.columns),
            "sample_data": df.head().to_dict('records'),
            "dtypes": df.dtypes.astype(str).to_dict()
        }
    except Exception as e:
        raise Exception(f"Failed to load CSV file: {str(e)}")

@tool
def execute_python(code: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute Python code in a sandboxed environment with access to loaded data.
    
    Args:
        code (str): Python code to execute
        data (Dict): Data loaded from CSV file
        
    Returns:
        Dict containing execution results and any generated charts
    """
    # Create a safe execution environment
    local_vars = {
        'df': data.get('df'),
        'pd': pd,
        'plt': plt,
        'sns': sns,
        'data': data
    }
    
    # Add the data to the local namespace
    if 'df' in data:
        local_vars['df'] = data['df']
    
    try:
        # Execute the code
        exec(code, globals(), local_vars)
        
        # Check if any charts were generated
        chart_data = None
        if 'plt' in local_vars and hasattr(local_vars['plt'], 'gcf'):
            # If matplotlib figures were created, save them
            fig = plt.gcf()
            if fig.get_axes():
                # Save chart to base64
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                chart_data = base64.b64encode(buffer.read()).decode('utf-8')
                plt.close()
        
        return {
            "success": True,
            "output": "Code executed successfully",
            "chart": chart_data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@tool
def save_chart(chart_data: str, filename: str) -> str:
    """
    Save chart data to a file.
    
    Args:
        chart_data (str): Base64 encoded chart data
        filename (str): Name of the file to save
        
    Returns:
        str: Path to saved file
    """
    try:
        # Decode base64 chart data
        chart_bytes = base64.b64decode(chart_data)
        
        # Save to file
        with open(filename, 'wb') as f:
            f.write(chart_bytes)
        
        return f"Chart saved to {filename}"
    except Exception as e:
        raise Exception(f"Failed to save chart: {str(e)}")

# Code Interpreter Sandbox

A data analysis agent that executes Python snippets against uploaded CSV files and returns charts and tables.

## Overview

This agent allows users to analyze CSV data through natural language prompts. It provides tools to load CSV files, execute Python code for data analysis, and generate visualizations. The agent uses GPT-4.1 for reasoning and can create charts using matplotlib and seaborn.

## Tools

### 1. `load_csv`
- **Purpose**: Load a CSV file and return metadata
- **Parameters**:
  - `file_path` (str): Path to the CSV file
- **Returns**: File information, column names, data types, and sample data

### 2. `execute_python`
- **Purpose**: Execute Python code with access to loaded data
- **Parameters**:
  - `code` (str): Python code to execute
  - `data` (Dict): Data loaded from CSV file
- **Returns**: Execution results and any generated charts

### 3. `save_chart`
- **Purpose**: Save generated charts to files
- **Parameters**:
  - `chart_data` (str): Base64 encoded chart data
  - `filename` (str): Name of the file to save
- **Returns**: Path to saved file

## Required Environment Variables

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your environment:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

3. Run the agent:
```bash
python main.py
```

## Example Usage

```
> Load the sales_data.csv file and show me a bar chart of sales by region
> Analyze the customer demographics in the customer_data.csv file
> Create a line chart showing monthly revenue trends
```

## Features

- **CSV Loading**: Automatically detects file structure and data types
- **Code Execution**: Safe execution environment for Python analysis
- **Chart Generation**: Creates visualizations using matplotlib/seaborn
- **File Management**: Saves charts to disk
- **Natural Language Interface**: Easy-to-use conversational interface

## Security

This agent runs in a sandboxed environment with limited access to system resources. It only executes code provided by the user and cannot access external resources beyond what's explicitly allowed by the tools.

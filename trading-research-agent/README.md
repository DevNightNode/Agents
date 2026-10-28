# Trading Research Agent

A market research agent that pulls stock quotes, news, computes technical indicators, and generates daily market briefs.

## Overview

This agent uses the Google ADK framework to create an intelligent trading research assistant. It can analyze stock symbols by fetching real-time data, computing technical indicators, and generating comprehensive market briefs.

## Tools

### 1. `get_quote(symbol: str)`
Fetches the latest stock quote for a given symbol.

**Parameters:**
- `symbol` (str): Stock symbol (e.g., 'AAPL', 'MSFT')

**Returns:**
```json
{
  "symbol": "AAPL",
  "price": 175.43,
  "change": 2.15,
  "change_percent": "+1.24%",
  "volume": 45678900,
  "latest_trading_day": "2023-06-15"
}
```

### 2. `get_news(symbol: str, limit: int = 5)`
Retrieves recent news articles for a stock symbol.

**Parameters:**
- `symbol` (str): Stock symbol
- `limit` (int): Number of articles to return (default: 5)

**Returns:**
```json
{
  "symbol": "AAPL",
  "articles": [
    {
      "title": "Apple Announces New Product Line",
      "source": "Financial Times",
      "url": "https://example.com/article",
      "published_time": "2023-06-15T10:30:00Z",
      "sentiment": 0.75
    }
  ]
}
```

### 3. `compute_indicators(symbol: str, period: int = 30)`
Computes technical indicators for a stock over a specified period.

**Parameters:**
- `symbol` (str): Stock symbol
- `period` (int): Number of days to analyze (default: 30)

**Returns:**
```json
{
  "symbol": "AAPL",
  "period": 30,
  "moving_average_20": 172.45,
  "moving_average_50": 168.23,
  "rsi": 62.34,
  "macd": 2.15,
  "macd_signal": 1.87,
  "price": 175.43
}
```

### 4. `write_brief(symbol: str, indicators: Dict, news: Dict)`
Generates a formatted daily market brief.

**Parameters:**
- `symbol` (str): Stock symbol
- `indicators` (Dict): Technical indicators from `compute_indicators`
- `news` (Dict): News articles from `get_news`

**Returns:**
```json
{
  "symbol": "AAPL",
  "brief": "Market Brief for AAPL\n========================\n\nPrice: $175.43\nMoving Averages:\n  - 20-day MA: $172.45\n  - 50-day MA: $168.23\n\nTechnical Indicators:\n  - RSI: 62.34\n  - MACD: 2.15\n  - MACD Signal: 1.87\n\nRecent News:\n  - Apple Announces New Product Line\n    Source: Financial Times\n    Sentiment: 0.750\n    Published: 2023-06-15T10:30:00Z\n"
}
```

## Required Environment Variables

Create a `.env` file with:
```
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

Get a free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key)

## Installation

```bash
pip install -r requirements.txt
```

## Running the Agent

```bash
python main.py
```

The agent will start and wait for user input. Example queries:
- "Analyze AAPL for me"
- "Research MSFT and give me a brief"
- "Get news and indicators for TSLA"

## Features

- Real-time stock data fetching
- Technical indicator computation (RSI, MACD, Moving Averages)
- News sentiment analysis
- Formatted daily market briefs
- Interactive command-line interface
- Error handling and validation

## Architecture

The agent uses the Google ADK framework with:
- Gemini 2.0 Flash model for reasoning
- Four custom tools implemented with proper typing
- In-memory runner for execution
- Environment-based configuration
- Comprehensive error handling

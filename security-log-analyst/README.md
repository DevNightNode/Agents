# Security Log Analyst Agent

A SOC analyst agent that queries Elasticsearch for auth logs, enriches IPs via an IP-reputation API, and blocks IPs via firewall API.

## Overview

This agent automates security log analysis by:
1. Searching authentication logs in Elasticsearch for failed login attempts
2. Enriching suspicious IP addresses with reputation information
3. Blocking malicious IPs via firewall API
4. Creating security incidents for suspicious activities

## Tools

### 1. `search_logs`
- **Description**: Searches authentication logs in Elasticsearch for failed login attempts within a specified time range
- **Parameters**:
  - `start_time` (string, required): Start time for the search in ISO format
  - `end_time` (string, required): End time for the search in ISO format
  - `limit` (integer, optional): Maximum number of results to return (default: 100)

### 2. `lookup_ip_reputation`
- **Description**: Looks up the IP's abuse confidence score on AbuseIPDB
- **Parameters**:
  - `ip_address` (string, required): The IP address to look up

### 3. `block_ip`
- **Description**: Blocks an IP address with a Cloudflare IP access rule
- **Parameters**:
  - `ip_address` (string, required): The IP address to block
  - `reason` (string, required): Reason for blocking the IP address

### 4. `create_incident`
- **Description**: Opens a security incident as a TheHive case
- **Parameters**:
  - `title` (string, required): Title of the incident
  - `description` (string, required): Description of the incident
  - `severity` (string, required): Severity level (low, medium, high, critical)
  - `ip_addresses` (array, optional): List of IP addresses involved in the incident

## Required Environment Variables

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key

# Elasticsearch connection
ELASTICSEARCH_HOST=http://localhost:9200
ELASTICSEARCH_USERNAME=elastic
ELASTICSEARCH_PASSWORD=your_password
AUTH_LOG_INDEX=auth-logs-*

# AbuseIPDB (IP reputation)
ABUSEIPDB_API_KEY=your_abuseipdb_key

# Cloudflare (IP access rules)
CLOUDFLARE_API_TOKEN=your_cloudflare_token
CLOUDFLARE_ZONE_ID=your_zone_id

# TheHive (incident cases)
THEHIVE_URL=https://thehive.example.internal
THEHIVE_API_KEY=your_thehive_api_key
```

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

The agent will automatically:
1. Search for failed authentication attempts in the last hour
2. Enrich suspicious IPs with reputation data
3. Block malicious IPs
4. Create security incidents for the activity

## Requirements

- Python 3.8+
- Elasticsearch 8.x
- IP reputation API access
- Firewall API access
- OpenAI API key (configured via environment variables)

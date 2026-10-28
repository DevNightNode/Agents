# Claude Ops Runbook Agent

An incident response agent that helps with operational tasks using the Claude Agent SDK. This agent can query metrics, retrieve incident details, acknowledge incidents, and restart services.

## Features

- **Query Datadog Metrics**: Retrieve metrics data for monitoring system health
- **Get PagerDuty Incidents**: Retrieve detailed incident information
- **Acknowledge Incidents**: Acknowledge PagerDuty incidents
- **Restart Services**: Restart system services using systemctl

## Tools

### `query_metrics`
Query Datadog metrics for a given metric name and timeframe.

**Parameters:**
- `metric_name` (str): The name of the metric to query
- `start_time` (str): Start time in Unix timestamp or relative time (e.g., "-1h")
- `end_time` (str): End time in Unix timestamp or relative time (e.g., "now")
- `query` (str): The query to filter metrics

### `get_incident`
Get details of a PagerDuty incident by ID.

**Parameters:**
- `incident_id` (str): The ID of the incident to retrieve

### `acknowledge_incident`
Acknowledge a PagerDuty incident by ID.

**Parameters:**
- `incident_id` (str): The ID of the incident to acknowledge

### `restart_service`
Restart a service by name.

**Parameters:**
- `service_name` (str): The name of the service to restart

## Required Environment Variables

Create a `.env` file with the following variables:

```env
DATADOG_API_KEY=your_datadog_api_key_here
DATADOG_APP_KEY=your_datadog_application_key
PAGERDUTY_API_KEY=your_pagerduty_api_key_here
PAGERDUTY_FROM_EMAIL=oncall@example.com
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env` file

3. Run the agent:
```bash
python main.py "Triage PagerDuty incident Q1ABC2DEF3 and restart the web service if the runbook calls for it"
```

## Usage

The agent can be used to help with incident response tasks. When prompted, it will:
1. Retrieve incident details from PagerDuty
2. Query relevant metrics from Datadog
3. Acknowledge incidents if needed
4. Restart services when required

Example usage:
```
Help me with incident ABC123. Check metrics and restart the web service if needed.
```

## Security

This agent has limited permissions and can only execute the defined tools. It requires proper API keys to be configured for external services.

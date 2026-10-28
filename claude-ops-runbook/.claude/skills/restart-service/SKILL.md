---
name: restart-service
description: Safely restart a systemd service on an ops host during an incident, after checking metrics and acknowledging the page. Use when an incident's runbook calls for a service restart.
allowed-tools: mcp__claude-ops-runbook__query_metrics, mcp__claude-ops-runbook__get_incident, mcp__claude-ops-runbook__acknowledge_incident, Bash(./scripts/restart-service.sh:*)
---

# Restart a service during an incident

1. Fetch the incident with `get_incident` and confirm which service it names.
2. Query the service's error rate and latency for the last 15 minutes with
   `query_metrics` (for example `avg:trace.http.request.errors{service:<name>}`).
3. Acknowledge the incident with `acknowledge_incident` so the on-call
   engineer knows someone is acting on it.
4. Ask the user to confirm the restart, naming the service and host.
5. Run `./scripts/restart-service.sh <service>` and report its output.
6. Re-query the same metrics after two minutes and say whether they recovered.

Never restart a database (`postgresql`, `mysql`, `redis`) with this skill;
escalate those to the database on-call instead.

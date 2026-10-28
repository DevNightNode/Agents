import os
import logging
from typing import Any, Dict, List, Optional

import requests
from elasticsearch import Elasticsearch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Elasticsearch client
es_client = Elasticsearch(
    os.getenv("ELASTICSEARCH_HOST", "http://localhost:9200"),
    basic_auth=(os.getenv("ELASTICSEARCH_USERNAME", ""), os.getenv("ELASTICSEARCH_PASSWORD", "")),
    request_timeout=30,
    max_retries=3,
    retry_on_timeout=True,
)
AUTH_LOG_INDEX = os.getenv("AUTH_LOG_INDEX", "auth-logs-*")

# AbuseIPDB (IP reputation)
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")

# Cloudflare (firewall IP access rules)
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID")

# TheHive (incident management)
THEHIVE_URL = os.getenv("THEHIVE_URL")
THEHIVE_API_KEY = os.getenv("THEHIVE_API_KEY")

SEVERITY = {"low": 1, "medium": 2, "high": 3, "critical": 4}


async def search_logs(start_time: str, end_time: str, limit: int = 100) -> Dict[str, Any]:
    """
    Search authentication logs in Elasticsearch for failed login attempts.

    Args:
        start_time: Start of the window, ISO 8601 or Elasticsearch date math (e.g. "now-1h")
        end_time: End of the window, ISO 8601 or date math (e.g. "now")
        limit: Maximum number of log events to return

    Returns:
        The failed attempts, plus a count of attempts per source IP
    """
    try:
        response = es_client.search(
            index=AUTH_LOG_INDEX,
            query={
                "bool": {
                    "filter": [
                        {"term": {"event.outcome": "failure"}},
                        {"term": {"event.category": "authentication"}},
                        {"range": {"@timestamp": {"gte": start_time, "lte": end_time}}},
                    ]
                }
            },
            size=limit,
            sort=[{"@timestamp": {"order": "desc"}}],
        )

        events = []
        counts: Dict[str, int] = {}
        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            ip = source.get("source", {}).get("ip")
            user = source.get("user", {}).get("name")
            events.append({"timestamp": source.get("@timestamp"), "ip": ip, "user": user})
            if ip:
                counts[ip] = counts.get(ip, 0) + 1

        logger.info(f"Found {len(events)} failed login attempts")
        return {
            "status": "success",
            "total_count": response["hits"]["total"]["value"],
            "attempts_by_ip": counts,
            "events": events,
        }
    except Exception as e:
        logger.error(f"Error searching logs: {e}")
        return {"status": "error", "error": str(e)}


async def lookup_ip_reputation(ip_address: str) -> Dict[str, Any]:
    """
    Look up an IP address's abuse reputation on AbuseIPDB.

    Args:
        ip_address: The IPv4 or IPv6 address to check

    Returns:
        Abuse confidence score (0-100), report count, country, ISP and usage type
    """
    if not ABUSEIPDB_API_KEY:
        return {"status": "error", "error": "ABUSEIPDB_API_KEY environment variable not set"}

    try:
        response = requests.get(
            "https://api.abuseipdb.com/api/v2/check",
            headers={"Key": ABUSEIPDB_API_KEY, "Accept": "application/json"},
            params={"ipAddress": ip_address, "maxAgeInDays": 90},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()["data"]
        return {
            "status": "success",
            "ip_address": ip_address,
            "abuse_confidence_score": data.get("abuseConfidenceScore"),
            "total_reports": data.get("totalReports"),
            "country": data.get("countryCode"),
            "isp": data.get("isp"),
            "usage_type": data.get("usageType"),
            "is_whitelisted": data.get("isWhitelisted"),
        }
    except Exception as e:
        logger.error(f"Error looking up IP reputation for {ip_address}: {e}")
        return {"status": "error", "error": str(e)}


async def block_ip(ip_address: str, reason: str) -> Dict[str, Any]:
    """
    Block an IP address at the edge with a Cloudflare IP access rule.

    Args:
        ip_address: The IP address to block
        reason: Why the IP is being blocked (stored as the rule's notes)

    Returns:
        The created access rule
    """
    if not CLOUDFLARE_API_TOKEN or not CLOUDFLARE_ZONE_ID:
        return {"status": "error", "error": "CLOUDFLARE_API_TOKEN and CLOUDFLARE_ZONE_ID must be set"}

    try:
        response = requests.post(
            f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/firewall/access_rules/rules",
            headers={"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"},
            json={
                "mode": "block",
                "configuration": {"target": "ip", "value": ip_address},
                "notes": reason,
            },
            timeout=10,
        )
        body = response.json()
        if not body.get("success"):
            return {"status": "error", "error": body.get("errors")}
        return {"status": "success", "ip_address": ip_address, "rule_id": body["result"]["id"]}
    except Exception as e:
        logger.error(f"Error blocking IP {ip_address}: {e}")
        return {"status": "error", "error": str(e)}


async def create_incident(
    title: str,
    description: str,
    severity: str,
    ip_addresses: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Open a security incident as a case in TheHive.

    Args:
        title: Title of the incident
        description: What happened, the evidence, and the actions taken
        severity: One of low, medium, high, critical
        ip_addresses: IP addresses involved, added to the case as tags

    Returns:
        The created case's ID and number
    """
    if not THEHIVE_URL or not THEHIVE_API_KEY:
        return {"status": "error", "error": "THEHIVE_URL and THEHIVE_API_KEY must be set"}
    if severity not in SEVERITY:
        return {"status": "error", "error": f"severity must be one of {', '.join(SEVERITY)}"}

    try:
        response = requests.post(
            f"{THEHIVE_URL.rstrip('/')}/api/v1/case",
            headers={"Authorization": f"Bearer {THEHIVE_API_KEY}"},
            json={
                "title": title,
                "description": description,
                "severity": SEVERITY[severity],
                "tags": ["soc-agent"] + [f"ip:{ip}" for ip in (ip_addresses or [])],
            },
            timeout=10,
        )
        response.raise_for_status()
        case = response.json()
        return {"status": "success", "case_id": case.get("_id"), "case_number": case.get("number")}
    except Exception as e:
        logger.error(f"Error creating incident: {e}")
        return {"status": "error", "error": str(e)}


# Exported for AssistantAgent(tools=...)
tools = [search_logs, lookup_ip_reputation, block_ip, create_incident]

#!/bin/bash
# Simple script to restart a service
# Usage: ./restart-service.sh <service_name>

SERVICE_NAME=$1

if [ -z "$SERVICE_NAME" ]; then
    echo "Usage: $0 <service_name>"
    exit 1
fi

echo "Restarting service: $SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"
echo "Service $SERVICE_NAME restarted."

# DevOps Kubernetes Operator Agent

A CrewAI-powered DevOps agent that inspects Kubernetes workloads, tails pod logs, and can restart or scale deployments.

## Overview

This agent provides a comprehensive set of tools for Kubernetes operations. It can inspect all pods in a cluster, tail logs from specific pods, restart deployments by deleting their pods, and scale deployments to a specified number of replicas.

## Tools

### 1. Get Pods
- **Description**: Retrieves information about all pods in the cluster
- **Parameters**: None
- **Output**: List of dictionaries containing pod name, namespace, status, node, and restart count

### 2. Get Pod Logs
- **Description**: Retrieves logs from a specific pod
- **Parameters**:
  - `pod_name` (str): Name of the pod
  - `namespace` (str): Namespace of the pod (default: "default")
  - `tail_lines` (int): Number of lines to show from the end of the logs (default: 50)
- **Output**: String containing the pod logs with timestamps

### 3. Restart Deployment
- **Description**: Restarts a deployment by deleting all its pods
- **Parameters**:
  - `deployment_name` (str): Name of the deployment to restart
  - `namespace` (str): Namespace of the deployment (default: "default")
- **Output**: Confirmation that the deployment has been restarted

### 4. Scale Deployment
- **Description**: Scales a deployment to the specified number of replicas
- **Parameters**:
  - `deployment_name` (str): Name of the deployment to scale
  - `namespace` (str): Namespace of the deployment (default: "default")
  - `replicas` (int): Number of replicas to scale to (default: 1)
- **Output**: Confirmation that the deployment has been scaled

## Required Environment Variables

This agent requires a valid Kubernetes configuration file. The agent will automatically detect if it's running inside a cluster or if it should use the local kubeconfig file.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your Kubernetes configuration:
   - Either place a `~/.kube/config` file in your home directory
   - Or run the agent inside a Kubernetes cluster with appropriate RBAC permissions

## Running the Agent

```bash
python main.py
```

The agent will execute a series of tasks demonstrating its capabilities. You can modify the inputs in `main.py` to test different scenarios.

## Security Considerations

This agent has full read and write access to your Kubernetes cluster. Ensure that:
1. The agent runs with appropriate RBAC permissions
2. The Kubernetes configuration is secure
3. Access to the agent is restricted in production environments

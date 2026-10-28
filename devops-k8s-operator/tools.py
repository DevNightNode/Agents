import os
from datetime import datetime, timezone
from typing import List, Dict, Any
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from crewai.tools import tool

# Initialize Kubernetes configuration
def init_k8s():
    try:
        config.load_incluster_config()
    except config.ConfigException:
        config.load_kube_config(context=os.getenv("KUBE_CONTEXT"))

# Initialize Kubernetes client
init_k8s()
v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

@tool("Get Pods")
def get_pods() -> List[Dict[str, Any]]:
    """
    Get all pods in the cluster with their status and details.
    
    Returns:
        List of dictionaries containing pod information including name, namespace, 
        status, node, and restart count.
    """
    try:
        pods = v1.list_pod_for_all_namespaces(watch=False)
        pod_list = []
        for pod in pods.items:
            pod_info = {
                "name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "status": pod.status.phase,
                "node": pod.spec.node_name,
                "restart_count": sum([container.restart_count for container in pod.status.container_statuses or []])
            }
            pod_list.append(pod_info)
        return pod_list
    except ApiException as e:
        return [{"error": f"Failed to get pods: {e}"}]

@tool("Get Pod Logs")
def get_pod_logs(pod_name: str, namespace: str = "default", tail_lines: int = 50) -> str:
    """
    Get logs from a specific pod.
    
    Args:
        pod_name (str): Name of the pod
        namespace (str): Namespace of the pod (default: "default")
        tail_lines (int): Number of lines to show from the end of the logs (default: 50)
    
    Returns:
        String containing the pod logs
    """
    try:
        logs = v1.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            tail_lines=tail_lines,
            timestamps=True
        )
        return logs
    except ApiException as e:
        return f"Failed to get logs for pod {pod_name}: {e}"

@tool("Restart Deployment")
def restart_deployment(deployment_name: str, namespace: str = "default") -> str:
    """
    Restart a deployment with a rolling restart (like kubectl rollout restart).
    
    Args:
        deployment_name (str): Name of the deployment to restart
        namespace (str): Namespace of the deployment (default: "default")
    
    Returns:
        String describing the restart action
    """
    try:
        # Same as `kubectl rollout restart`: bump the pod template annotation so
        # the deployment rolls its pods according to its update strategy.
        now = datetime.now(timezone.utc).isoformat()
        apps_v1.patch_namespaced_deployment(
            name=deployment_name,
            namespace=namespace,
            body={"spec": {"template": {"metadata": {"annotations": {
                "kubectl.kubernetes.io/restartedAt": now
            }}}}}
        )
        return f"Rolling restart of deployment {deployment_name} in {namespace} started at {now}"
    except ApiException as e:
        return f"Failed to restart deployment {deployment_name}: {e}"

@tool("Scale Deployment")
def scale_deployment(deployment_name: str, namespace: str = "default", replicas: int = 1) -> str:
    """
    Scale a deployment to the specified number of replicas.
    
    Args:
        deployment_name (str): Name of the deployment to scale
        namespace (str): Namespace of the deployment (default: "default")
        replicas (int): Number of replicas to scale to (default: 1)
    
    Returns:
        String describing the scaling action
    """
    try:
        # Get current deployment
        deployment = apps_v1.read_namespaced_deployment(
            name=deployment_name,
            namespace=namespace
        )
        
        # Update replicas
        deployment.spec.replicas = replicas
        
        # Apply the update
        apps_v1.patch_namespaced_deployment(
            name=deployment_name,
            namespace=namespace,
            body=deployment
        )
        
        return f"Scaled deployment {deployment_name} in namespace {namespace} to {replicas} replicas."
    except ApiException as e:
        return f"Failed to scale deployment {deployment_name}: {e}"

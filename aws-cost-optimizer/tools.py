import boto3
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from agents import function_tool

@function_tool
def list_idle_instances() -> List[Dict[str, Any]]:
    """
    Lists EC2 instances that are currently running but not receiving any traffic.
    Returns a list of dictionaries containing instance details.
    """
    ec2 = boto3.client('ec2')
    
    # Get all running instances
    paginator = ec2.get_paginator('describe_instances')
    pages = paginator.paginate(
        Filters=[
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )
    reservations = [r for page in pages for r in page['Reservations']]
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=7)
    
    idle_instances = []
    
    for reservation in reservations:
        for instance in reservation['Instances']:
            # Check if instance has any network activity
            instance_id = instance['InstanceId']
            
            # Get instance metrics for CPU utilization
            try:
                cloudwatch = boto3.client('cloudwatch')
                metrics = cloudwatch.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='CPUUtilization',
                    Dimensions=[
                        {
                            'Name': 'InstanceId',
                            'Value': instance_id
                        }
                    ],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=86400,
                    Statistics=['Average']
                )
                
                # If no metrics or low CPU usage, consider it idle
                points = metrics['Datapoints']
                cpu_avg = sum(p['Average'] for p in points) / len(points) if points else 0
                
                if cpu_avg < 10:  # Less than 10% CPU usage
                    idle_instances.append({
                        'instance_id': instance_id,
                        'instance_type': instance['InstanceType'],
                        'launch_time': instance['LaunchTime'].isoformat(),
                        'vpc_id': instance.get('VpcId', 'N/A'),
                        'subnet_id': instance.get('SubnetId', 'N/A'),
                        'cpu_utilization': cpu_avg
                    })
            except Exception:
                # If we can't get metrics, still include the instance
                idle_instances.append({
                    'instance_id': instance_id,
                    'instance_type': instance['InstanceType'],
                    'launch_time': instance['LaunchTime'].isoformat(),
                    'vpc_id': instance.get('VpcId', 'N/A'),
                    'subnet_id': instance.get('SubnetId', 'N/A'),
                    'cpu_utilization': 'Unknown'
                })
    
    return idle_instances

@function_tool
def list_unattached_volumes() -> List[Dict[str, Any]]:
    """
    Lists EBS volumes that are not attached to any EC2 instance.
    Returns a list of dictionaries containing volume details.
    """
    ec2 = boto3.client('ec2')
    
    # Get all volumes
    paginator = ec2.get_paginator('describe_volumes')
    volumes = [v for page in paginator.paginate() for v in page['Volumes']]
    
    unattached_volumes = []
    
    for volume in volumes:
        # Check if volume is attached
        if not volume['Attachments']:
            volume_id = volume['VolumeId']
            volume_size = volume['Size']
            volume_type = volume['VolumeType']
            creation_time = volume['CreateTime']
            
            # Get volume details
            try:
                # Get volume tags for additional information
                tags = {tag['Key']: tag['Value'] for tag in volume.get('Tags', [])}
                
                unattached_volumes.append({
                    'volume_id': volume_id,
                    'volume_size': volume_size,
                    'volume_type': volume_type,
                    'creation_time': creation_time.isoformat(),
                    'tags': tags
                })
            except Exception:
                unattached_volumes.append({
                    'volume_id': volume_id,
                    'volume_size': volume_size,
                    'volume_type': volume_type,
                    'creation_time': creation_time.isoformat(),
                    'tags': {}
                })
    
    return unattached_volumes

@function_tool
def stop_instance(instance_id: str) -> Dict[str, Any]:
    """
    Stops an EC2 instance by its instance ID.
    
    Args:
        instance_id (str): The ID of the EC2 instance to stop
        
    Returns:
        Dict containing the result of the stop operation
    """
    ec2 = boto3.client('ec2')
    
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id])
        return {
            'status': 'success',
            'message': f'Instance {instance_id} stopped successfully',
            'response': response
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to stop instance {instance_id}: {str(e)}'
        }

@function_tool
def delete_volume(volume_id: str) -> Dict[str, Any]:
    """
    Deletes an EBS volume by its volume ID.
    
    Args:
        volume_id (str): The ID of the EBS volume to delete
        
    Returns:
        Dict containing the result of the delete operation
    """
    ec2 = boto3.client('ec2')
    
    try:
        response = ec2.delete_volume(VolumeId=volume_id)
        return {
            'status': 'success',
            'message': f'Volume {volume_id} deleted successfully',
            'response': response
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to delete volume {volume_id}: {str(e)}'
        }

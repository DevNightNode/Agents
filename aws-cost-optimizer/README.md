# AWS Cost Optimizer Agent

An AI agent that helps optimize AWS costs by identifying idle EC2 instances and unattached EBS volumes, and providing the ability to stop or delete these resources.

## Features

- **Idle Instance Detection**: Identifies running EC2 instances with low CPU utilization
- **Unattached Volume Detection**: Finds EBS volumes not attached to any EC2 instance
- **Cost Optimization Actions**: Stop idle instances and delete unattached volumes
- **Savings Estimation**: Provides estimates of potential cost savings

## Tools

1. `list_idle_instances()` - Lists EC2 instances with low CPU utilization (less than 10%)
2. `list_unattached_volumes()` - Lists EBS volumes not attached to any EC2 instance
3. `stop_instance(instance_id)` - Stops a specified EC2 instance
4. `delete_volume(volume_id)` - Deletes a specified EBS volume

## Required Environment Variables

Create a `.env` file with the following variables:

```env
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_DEFAULT_REGION=us-east-1
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

The agent will prompt for input. Examples of commands:

- "List my idle EC2 instances"
- "Show me unattached EBS volumes"
- "Stop instance i-1234567890abcdef0"
- "Delete volume vol-1234567890abcdef0"

## How It Works

1. The agent uses boto3 to connect to AWS services
2. For idle instances, it checks CPU utilization via CloudWatch metrics
3. For unattached volumes, it queries the EBS service directly
4. When taking action, it confirms with the user before proceeding
5. All actions are logged and reported back to the user

## Security Notes

- This agent requires AWS credentials with appropriate permissions
- It only performs read operations by default
- Write operations (stop/delete) require explicit user confirmation
- Ensure your AWS credentials are secure and have minimal required permissions

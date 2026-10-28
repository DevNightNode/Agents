# Terraform Plan Reviewer

A Go MCP server that provides tools for reviewing and applying Terraform plans. This agent can run `terraform plan -json`, read `.tf` files, and apply saved plans.

## Features

- **run_plan**: Executes `terraform plan -json` in a specified working directory
- **read_tf_file**: Reads and returns the content of a Terraform file
- **apply_plan**: Applies a saved Terraform plan file

## Tools

### run_plan
Runs `terraform plan -json` and returns the JSON output.

**Arguments:**
- `working_dir` (required): Path to the Terraform working directory
- `tf_vars` (optional): Path to Terraform variables file

### read_tf_file
Reads and returns the content of a Terraform file.

**Arguments:**
- `file_path` (required): Path to the Terraform file

### apply_plan
Applies a saved Terraform plan file.

**Arguments:**
- `plan_file` (required): Path to the Terraform plan file
- `working_dir` (required): Path to the Terraform working directory

## Requirements

- Go 1.22+
- Terraform CLI installed and accessible in PATH
- Working directory with valid Terraform configuration

## Environment Variables

No environment variables required.

## Running

1. Build the agent:
   ```bash
   go build -o terraform-plan-reviewer .
   ```

2. Run the agent:
   ```bash
   ./terraform-plan-reviewer
   ```

## Usage Example

```bash
# Run a plan
./terraform-plan-reviewer run_plan --working_dir=/path/to/terraform --tf_vars=/path/to/variables.tf

# Read a Terraform file
./terraform-plan-reviewer read_tf_file --file_path=/path/to/main.tf

# Apply a plan
./terraform-plan-reviewer apply_plan --plan_file=/path/to/plan.out --working_dir=/path/to/terraform
```

## Security Notes

This agent directly executes Terraform commands. Ensure that:
1. The working directory is properly secured
2. Only authorized users can access the agent
3. The agent runs in a secure environment with appropriate permissions

package main

import (
	"context"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
)

func main() {
	s := server.NewMCPServer("terraform-plan-reviewer", "1.0.0")

	s.AddTool(
		mcp.NewTool("run_plan", mcp.WithDescription("Runs terraform plan, saves it to tfplan in the working directory, and returns the JSON plan output"),
			mcp.WithString("working_dir", mcp.Required(), mcp.Description("Path to the Terraform working directory")),
			mcp.WithString("tf_vars", mcp.Description("Path to Terraform variables file")),
		),
		runPlanHandler,
	)

	s.AddTool(
		mcp.NewTool("read_tf_file", mcp.WithDescription("Reads and returns the content of a Terraform file"),
			mcp.WithString("file_path", mcp.Required(), mcp.Description("Path to the Terraform file")),
		),
		readTfFileHandler,
	)

	s.AddTool(
		mcp.NewTool("apply_plan", mcp.WithDescription("Applies a saved Terraform plan file"),
			mcp.WithString("plan_file", mcp.Required(), mcp.Description("Path to the Terraform plan file")),
			mcp.WithString("working_dir", mcp.Required(), mcp.Description("Path to the Terraform working directory")),
		),
		applyPlanHandler,
	)

	if err := server.ServeStdio(s); err != nil {
		fmt.Fprintf(os.Stderr, "Error starting server: %v\n", err)
		os.Exit(1)
	}
}

func runPlanHandler(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	workingDir, err := req.RequireString("working_dir")
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Missing required argument: working_dir. Error: %v", err)), nil
	}

	tfVars := req.GetString("tf_vars", "")

	// Check if working directory exists
	if _, err := os.Stat(workingDir); os.IsNotExist(err) {
		return mcp.NewToolResultError(fmt.Sprintf("Working directory does not exist: %s", workingDir)), nil
	}

	// Initialize terraform if needed
	cmd := exec.Command("terraform", "init", "-no-color")
	cmd.Dir = workingDir
	output, err := cmd.CombinedOutput()
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Failed to initialize terraform: %s", string(output))), nil
	}

	// Prepare plan command
	args := []string{"plan", "-json", "-no-color", "-out=tfplan"}
	if tfVars != "" {
		args = append(args, "-var-file="+tfVars)
	}

	cmd = exec.Command("terraform", args...)
	cmd.Dir = workingDir

	output, err = cmd.CombinedOutput()
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Failed to run terraform plan: %s", string(output))), nil
	}

	return mcp.NewToolResultText(string(output)), nil
}

func readTfFileHandler(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	filePath, err := req.RequireString("file_path")
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Missing required argument: file_path. Error: %v", err)), nil
	}

	// Check if file exists
	if _, err := os.Stat(filePath); os.IsNotExist(err) {
		return mcp.NewToolResultError(fmt.Sprintf("Terraform file does not exist: %s", filePath)), nil
	}

	// Check if file has .tf extension
	if !strings.HasSuffix(filePath, ".tf") {
		return mcp.NewToolResultError(fmt.Sprintf("File must have .tf extension: %s", filePath)), nil
	}

	content, err := os.ReadFile(filePath)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Failed to read Terraform file: %v", err)), nil
	}

	return mcp.NewToolResultText(string(content)), nil
}

func applyPlanHandler(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	planFile, err := req.RequireString("plan_file")
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Missing required argument: plan_file. Error: %v", err)), nil
	}

	workingDir, err := req.RequireString("working_dir")
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Missing required argument: working_dir. Error: %v", err)), nil
	}

	// Check if working directory exists
	if _, err := os.Stat(workingDir); os.IsNotExist(err) {
		return mcp.NewToolResultError(fmt.Sprintf("Working directory does not exist: %s", workingDir)), nil
	}

	// Check if plan file exists (relative paths are relative to the working directory)
	if !filepath.IsAbs(planFile) {
		planFile = filepath.Join(workingDir, planFile)
	}
	if _, err := os.Stat(planFile); os.IsNotExist(err) {
		return mcp.NewToolResultError(fmt.Sprintf("Plan file does not exist: %s", planFile)), nil
	}

	// Run terraform apply with plan file
	cmd := exec.Command("terraform", "apply", "-no-color", "-auto-approve", planFile)
	cmd.Dir = workingDir

	output, err := cmd.CombinedOutput()
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Failed to apply terraform plan: %s", string(output))), nil
	}

	return mcp.NewToolResultText(string(output)), nil
}

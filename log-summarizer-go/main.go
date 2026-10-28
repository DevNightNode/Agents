package main

import (
	"context"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"strings"
	"time"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
	"github.com/sirupsen/logrus"
)

type LogSummarizer struct {
	logger *logrus.Logger
}

func NewLogSummarizer() *LogSummarizer {
	return &LogSummarizer{
		logger: logrus.New(),
	}
}

func (ls *LogSummarizer) readLogs(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	logPath, err := req.RequireString("log_path")
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("missing required argument: log_path. Error: %v", err)), nil
	}

	lines, err := req.RequireString("lines")
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("missing required argument: lines. Error: %v", err)), nil
	}

	n, err := fmt.Sscanf(lines, "%d", new(int))
	if err != nil || n != 1 {
		return mcp.NewToolResultError("invalid lines argument, must be a number"), nil
	}

	// Check if file exists
	if _, err := os.Stat(logPath); os.IsNotExist(err) {
		return mcp.NewToolResultError(fmt.Sprintf("log file does not exist: %s", logPath)), nil
	}

	// Use tail command to read last N lines
	cmd := exec.CommandContext(ctx, "tail", "-n", lines, logPath)
	output, err := cmd.Output()
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("failed to read log file: %v", err)), nil
	}

	return mcp.NewToolResultText(string(output)), nil
}

func (ls *LogSummarizer) postWebhook(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	webhookURL, err := req.RequireString("webhook_url")
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("missing required argument: webhook_url. Error: %v", err)), nil
	}

	summary, err := req.RequireString("summary")
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("missing required argument: summary. Error: %v", err)), nil
	}

	// Create HTTP client with timeout
	client := &http.Client{
		Timeout: 10 * time.Second,
	}

	// Prepare POST request
	payload := fmt.Sprintf(`{"summary": %q}`, summary)
	reqBody := strings.NewReader(payload)

	httpReq, err := http.NewRequestWithContext(ctx, "POST", webhookURL, reqBody)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("failed to create request: %v", err)), nil
	}
	httpReq.Header.Set("Content-Type", "application/json")

	// Send POST request
	resp, err := client.Do(httpReq)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("failed to send webhook: %v", err)), nil
	}
	defer resp.Body.Close()

	if resp.StatusCode >= 300 {
		body, _ := io.ReadAll(resp.Body)
		return mcp.NewToolResultError(fmt.Sprintf("webhook returned status %d: %s", resp.StatusCode, string(body))), nil
	}

	return mcp.NewToolResultText("Webhook posted successfully"), nil
}

func main() {
	// Initialize server
	s := server.NewMCPServer("log-summarizer-go", "1.0.0")

	// Initialize log summarizer
	ls := NewLogSummarizer()

	// Read logs tool
	readLogsTool := mcp.NewTool("read_logs",
		mcp.WithDescription("Reads the last N lines from a log file"),
		mcp.WithString("log_path", mcp.Required(), mcp.Description("Path to the log file")),
		mcp.WithString("lines", mcp.Required(), mcp.Description("Number of lines to read from the end of the file")),
	)
	s.AddTool(readLogsTool, func(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		return ls.readLogs(ctx, req)
	})

	// Post webhook tool
	postWebhookTool := mcp.NewTool("post_webhook",
		mcp.WithDescription("Posts a summary to a webhook URL"),
		mcp.WithString("webhook_url", mcp.Required(), mcp.Description("URL of the webhook to post to")),
		mcp.WithString("summary", mcp.Required(), mcp.Description("Summary text to post")),
	)
	s.AddTool(postWebhookTool, func(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		return ls.postWebhook(ctx, req)
	})

	// Serve the MCP server
	server.ServeStdio(s)
}

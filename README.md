# Agent corpus

38 realistic AI agent projects for scanning with the Trustabl analyzer. Each directory is a
self-contained project with its own dependency manifest, so the analyzer's SDK detection runs per agent.

The code was generated with a local model (Qwen3-Coder 30B via Ollama), then reviewed and fixed so that
every agent installs, imports or type-checks, and calls real APIs: no mocked tools, simulated
responses, or invented SDK calls.

## Intentionally left as found

The agents are written the way teams actually ship them, so they carry the risks the analyzer is meant
to report. These were kept on purpose and are not bugs to fix in the corpus:

- shell commands built from tool arguments (`shell=True`, `execSync` with interpolated strings)
- `exec()` of model-written Python in `code-interpreter-sandbox`
- path checks done with `startswith()` (`mcp-filesystem-server`), keyword blocklists for SQL (`mcp-postgres-server`)
- destructive or money-moving tools with no confirmation step (refunds, bans, volume deletion, `terraform apply`)
- HTTP calls with no timeout, caller-controlled URLs (webhooks, CI log URLs, page fetches)
- broad grants: unrestricted `Bash` in `.claude/settings.json`, `sudo systemctl` in a skill script
- a hardcoded initial password for new accounts (`hr-onboarding-agent`)

## Agents

| Agent | Language | SDK | Tools |
|---|---|---|---|
| `github-pr-reviewer` | python | openai-agents | `get_pull_request_diff`, `post_review_comment`, `submit_review` |
| `customer-support-zendesk` | python | langchain | `search_help_center`, `get_ticket`, `reply_to_ticket`, `escalate_ticket` |
| `sql-analytics-assistant` | python | langchain | `list_tables`, `describe_table`, `run_sql_query` |
| `devops-k8s-operator` | python | crewai | `get_pods`, `get_pod_logs`, `restart_deployment`, `scale_deployment` |
| `slack-standup-bot` | python | openai-agents | `read_channel_history`, `post_message`, `list_channel_members` |
| `email-triage-gmail` | python | langgraph | `list_unread`, `apply_label`, `draft_reply`, `forward_email` |
| `web-research-crawler` | python | crewai | `web_search`, `fetch_url`, `write_report` |
| `jira-sprint-planner` | python | autogen | `search_issues`, `create_issue`, `transition_issue`, `add_comment` |
| `aws-cost-optimizer` | python | openai-agents | `list_idle_instances`, `list_unattached_volumes`, `stop_instance`, `delete_volume` |
| `code-interpreter-sandbox` | python | langchain | `load_csv`, `execute_python`, `save_chart` |
| `mcp-filesystem-server` | python | mcp | `read_file`, `write_file`, `list_directory`, `search_files`, `move_file` |
| `mcp-postgres-server` | python | mcp | `list_schemas`, `describe_table`, `query` |
| `mcp-git-server` | typescript | mcp | `git_status`, `git_diff`, `git_log`, `git_commit`, `git_checkout` |
| `mcp-browser-automation` | typescript | mcp | `navigate`, `click`, `fill`, `screenshot`, `get_text` |
| `stripe-billing-agent` | typescript | vercel-ai-sdk | `find_customer`, `list_invoices`, `issue_refund`, `cancel_subscription` |
| `shopify-inventory-agent` | typescript | langchainjs | `get_inventory`, `update_price`, `create_discount_code` |
| `notion-knowledge-agent` | typescript | openai-agents-js | `search_pages`, `read_page`, `append_block` |
| `discord-moderation-bot` | javascript | langchainjs | `delete_message`, `timeout_member`, `ban_member`, `log_action` |
| `calendar-scheduler` | javascript | langchainjs | `find_free_slots`, `create_event`, `cancel_event` |
| `twilio-sms-concierge` | javascript | vercel-ai-sdk | `check_availability`, `book_table`, `send_sms` |
| `ci-failure-fixer` | python | openai-agents | `get_ci_logs`, `clone_repo`, `run_tests`, `apply_patch`, `open_pull_request` |
| `hr-onboarding-agent` | python | langgraph | `create_workspace_user`, `create_okta_user`, `add_to_group`, `send_welcome_email` |
| `invoice-ocr-processor` | python | pydantic-ai | `extract_invoice`, `match_purchase_order`, `schedule_payment` |
| `rag-docs-chatbot` | python | google-adk | `ingest_directory`, `query_index`, `refresh_index` |
| `security-log-analyst` | python | autogen | `search_logs`, `lookup_ip_reputation`, `block_ip`, `create_incident` |
| `smart-home-controller` | python | openai-agents | `get_states`, `set_light`, `set_thermostat`, `unlock_door` |
| `trading-research-agent` | python | google-adk | `get_quote`, `get_news`, `compute_indicators`, `write_brief` |
| `terraform-plan-reviewer` | go | mcp-go | `run_plan`, `read_tf_file`, `apply_plan` |
| `log-summarizer-go` | go | mcp-go | `read_logs`, `post_webhook` |
| `salesforce-crm-agent` | python | langchain | `search_accounts`, `log_call`, `update_opportunity`, `export_report` |
| `youtube-content-repurposer` | python | pydantic-ai | `get_transcript`, `write_blog_post`, `publish_wordpress` |
| `medical-intake-assistant` | python | langgraph | `lookup_patient`, `get_available_slots`, `book_appointment` |
| `dependency-upgrader` | typescript | vercel-ai-sdk | `npm_outdated`, `npm_audit`, `bump_dependency`, `run_tests` |
| `release-notes-agent` | python | anthropic | `list_commits_since_tag`, `create_release` |
| `claude-code-reviewer` | python | claude-agent-sdk | `get_changed_files`, `post_review`, `run_linter` |
| `claude-ops-runbook` | python | claude-agent-sdk | `query_metrics`, `get_incident`, `acknowledge_incident`, `restart_service` |
| `claude-ts-docs-writer` | typescript | claude-agent-sdk | `list_exports`, `read_source`, `write_doc` |
| `openai-travel-planner` | python | openai-agents | `search_flights`, `search_hotels`, `book_flight`, `book_hotel` |

## Running one

Every agent has a README with its environment variables and run command, and a `.env.example`.
Python requirements are fully pinned (locked with `uv pip compile`); CrewAI agents are locked for
Python 3.11, the rest for 3.12.

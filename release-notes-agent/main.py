import json
import subprocess
import sys

import anthropic
from dotenv import load_dotenv

from tools import list_commits_since_tag, create_release

load_dotenv()

MODEL = "claude-sonnet-4-5"
MAX_ITERATIONS = 10

SYSTEM_PROMPT = """You write release notes for a git repository and publish them as a GitHub release.

1. Call list_commits_since_tag with the previous tag to get the commits in this release.
2. Group the commits into Features, Fixes, Performance, Documentation and Chores using
   their Conventional Commit prefixes; summarise merge commits by the change they bring in.
3. Write concise markdown release notes, one bullet per user-visible change, crediting authors.
4. Call create_release once with the new tag, a title, and the notes as the body.
Never invent commits that list_commits_since_tag did not return."""

TOOLS = [
    {
        "name": "list_commits_since_tag",
        "description": "List the commits on HEAD since a git tag. Returns sha, author and subject for each commit.",
        "input_schema": {
            "type": "object",
            "properties": {
                "tag": {"type": "string", "description": "The previous release tag, e.g. v1.4.0"},
            },
            "required": ["tag"],
        },
    },
    {
        "name": "create_release",
        "description": "Publish a GitHub release for the origin remote's repository.",
        "input_schema": {
            "type": "object",
            "properties": {
                "tag": {"type": "string", "description": "Tag name for the new release"},
                "title": {"type": "string", "description": "Release title"},
                "body": {"type": "string", "description": "Markdown release notes"},
                "is_prerelease": {"type": "boolean", "description": "Mark the release as a pre-release"},
            },
            "required": ["tag", "title", "body"],
        },
    },
]

HANDLERS = {
    "list_commits_since_tag": list_commits_since_tag,
    "create_release": create_release,
}


def latest_tag() -> str:
    result = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def run_tool(name: str, args: dict) -> str:
    try:
        return json.dumps(HANDLERS[name](**args), default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <new_tag>")
        sys.exit(1)
    new_tag = sys.argv[1]

    try:
        previous_tag = latest_tag()
    except subprocess.CalledProcessError:
        print("No previous git tag found; tag the last release first.")
        sys.exit(1)

    client = anthropic.Anthropic()
    messages = [{
        "role": "user",
        "content": f"Publish release {new_tag}. The previous release tag is {previous_tag}.",
    }]

    for _ in range(MAX_ITERATIONS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            for block in response.content:
                if block.type == "text":
                    print(block.text)
            return

        results = []
        for block in response.content:
            if block.type == "tool_use":
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": run_tool(block.name, block.input),
                })
        messages.append({"role": "user", "content": results})

    print(f"Stopped after {MAX_ITERATIONS} iterations without finishing.")
    sys.exit(1)


if __name__ == "__main__":
    main()

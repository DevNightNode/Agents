import os
from pydantic_ai import Agent, RunContext
from tools import Deps, get_transcript, write_blog_post, publish_wordpress

# Create agent with system prompt
agent = Agent(
    "openai:gpt-4",
    deps_type=Deps,
    system_prompt="""
    You are a content repurposing assistant that helps convert YouTube videos into blog posts and social media content.
    
    Your workflow:
    1. First, get the transcript from a YouTube video using get_transcript()
    2. Then, write a comprehensive blog post using write_blog_post()
    3. Finally, publish the blog post to WordPress using publish_wordpress()
    
    Always follow this exact sequence of steps when processing a YouTube video.
    """,
    tools=[get_transcript, write_blog_post, publish_wordpress]
)

if __name__ == "__main__":
    # Example usage
    video_url = input("Enter YouTube video URL: ").strip()
    
    if not video_url:
        print("No video URL provided")
        exit(1)
        
    try:
        # Run the agent with the video URL
        result = agent.run_sync(
            f"Process this YouTube video: {video_url}",
            deps=Deps()
        )
        print("Agent output:")
        print(result.output)
    except Exception as e:
        print(f"Error: {str(e)}")

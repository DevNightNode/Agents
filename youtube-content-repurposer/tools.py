import os
import re
from typing import Optional
from pydantic_ai import RunContext
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import requests
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods.taxonomies import GetTerms
from wordpress_xmlrpc.compat import xmlrpc_client

class Deps:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.wordpress_url = os.getenv('WORDPRESS_URL')
        self.wordpress_username = os.getenv('WORDPRESS_USERNAME')
        self.wordpress_password = os.getenv('WORDPRESS_PASSWORD')
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')

async def get_transcript(ctx: RunContext[Deps], video_url: str) -> str:
    """
    Download transcript from a YouTube video.
    
    Args:
        video_url: The full YouTube URL
        
    Returns:
        Transcript text
        
    Raises:
        Exception: If transcript is not available or API fails
    """
    # Extract video ID from URL
    video_id = None
    if 'youtu.be' in video_url:
        video_id = video_url.split('/')[-1]
    elif 'youtube.com' in video_url:
        match = re.search(r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})', video_url)
        if match:
            video_id = match.group(1)
    
    if not video_id:
        raise Exception("Invalid YouTube URL")
    
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])
        result = transcript.fetch()
        return ' '.join([item['text'] for item in result])
    except (TranscriptsDisabled, NoTranscriptFound):
        raise Exception("No transcript available for this video")
    except Exception as e:
        raise Exception(f"Failed to fetch transcript: {str(e)}")

async def write_blog_post(ctx: RunContext[Deps], transcript: str, title: str) -> str:
    """
    Write a blog post based on the transcript.
    
    Args:
        transcript: Transcript text from YouTube video
        title: Title for the blog post
        
    Returns:
        Generated blog post content
    """
    if not ctx.deps.openai_api_key:
        raise Exception("OPENAI_API_KEY not set")
        
    from openai import OpenAI
    client = OpenAI(api_key=ctx.deps.openai_api_key)
    
    prompt = f"""
    Write a comprehensive blog post based on the following YouTube transcript.
    The post should be engaging, informative, and well-structured with:
    - An introduction that hooks the reader
    - Clear sections with headings
    - Key takeaways
    - A conclusion
    - Proper formatting with paragraphs
    
    Title: {title}
    
    Transcript:
    {transcript}
    
    Write in a professional yet accessible tone appropriate for a blog audience.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a skilled content writer who creates engaging blog posts from transcripts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Failed to generate blog post: {str(e)}")

async def publish_wordpress(ctx: RunContext[Deps], content: str, title: str, post_type: str = "post") -> str:
    """
    Publish content to WordPress.
    
    Args:
        content: The content to publish
        title: The title for the post
        post_type: Type of post (post, page, etc.)
        
    Returns:
        URL of the published post
    """
    if not all([ctx.deps.wordpress_url, ctx.deps.wordpress_username, ctx.deps.wordpress_password]):
        raise Exception("WordPress credentials not set")
        
    try:
        client = Client(ctx.deps.wordpress_url + '/xmlrpc.php', ctx.deps.wordpress_username, ctx.deps.wordpress_password)
        
        post = {
            'post_type': post_type,
            'post_title': title,
            'post_content': content,
            'post_status': 'publish'
        }
        
        post_id = client.call(NewPost(post))
        return f"{ctx.deps.wordpress_url}/?p={post_id}"
    except Exception as e:
        raise Exception(f"Failed to publish to WordPress: {str(e)}")

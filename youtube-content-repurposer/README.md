# YouTube Content Repurposer

A Pydantic-AI agent that automatically converts YouTube videos into blog posts and publishes them to WordPress.

## Features

- Downloads transcripts from YouTube videos
- Generates engaging blog posts from video content
- Publishes content directly to WordPress
- Fully automated workflow from video to published post

## Tools

### 1. `get_transcript(video_url: str)`
Downloads the transcript from a YouTube video.

**Parameters:**
- `video_url` (str): Full YouTube URL

**Returns:**
- Transcript text as string

### 2. `write_blog_post(transcript: str, title: str)`
Writes a comprehensive blog post based on the transcript.

**Parameters:**
- `transcript` (str): Transcript text from YouTube video
- `title` (str): Title for the blog post

**Returns:**
- Generated blog post content as string

### 3. `publish_wordpress(content: str, title: str, post_type: str)`
Publishes content to WordPress.

**Parameters:**
- `content` (str): The content to publish
- `title` (str): The title for the post
- `post_type` (str): Type of post (default: "post")

**Returns:**
- URL of the published post

## Required Environment Variables

Create a `.env` file with the following variables:

```
OPENAI_API_KEY=your_openai_api_key_here
WORDPRESS_URL=https://your-wordpress-site.com
WORDPRESS_USERNAME=your_wordpress_username
WORDPRESS_PASSWORD=your_wordpress_password
YOUTUBE_API_KEY=your_youtube_api_key
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

When prompted, enter a YouTube video URL. The agent will:
1. Download the transcript
2. Generate a blog post
3. Publish to WordPress
4. Return the published post URL

## Requirements

- Python 3.8+
- OpenAI API key
- WordPress site with XML-RPC enabled
- YouTube API key (optional but recommended for better transcript availability)

import { tool } from '@openai/agents';
import { z } from 'zod';
import { Client } from '@notionhq/client';
import type { BlockObjectRequest } from '@notionhq/client/build/src/api-endpoints.js';

const notion = new Client({ auth: process.env.NOTION_TOKEN });

export const search_pages = tool({
  name: 'search_pages',
  description: 'Search for Notion pages by title or content',
  parameters: z.object({
    query: z.string().describe('Search query string'),
    limit: z.number().nullable().describe('Maximum number of results to return (default: 10)'),
  }),
  execute: async ({ query, limit }) => {
    try {
      const results = await notion.search({
        query,
        page_size: limit ?? 10,
        filter: { property: 'object', value: 'page' }
      });
      
      return results.results.map((page: any) => ({
        id: page.id,
        title: page.properties.title?.title?.[0]?.text?.content || 'Untitled',
        url: page.url,
        last_edited_time: page.last_edited_time
      }));
    } catch (error) {
      throw new Error(`Failed to search pages: ${error}`);
    }
  }
});

export const read_page = tool({
  name: 'read_page',
  description: 'Read the content of a Notion page',
  parameters: z.object({
    page_id: z.string().describe('The Notion page ID to read'),
  }),
  execute: async ({ page_id }) => {
    try {
      const pageContent = await notion.blocks.children.list({ block_id: page_id });
      
      const content = pageContent.results.map((block: any) => {
        const type = block.type;
        const content = block[type]?.text?.map((t: any) => t.plain_text).join(' ') || '';
        return `${type}: ${content}`;
      }).join('\n\n');
      
      return {
        page_id,
        content
      };
    } catch (error) {
      throw new Error(`Failed to read page: ${error}`);
    }
  }
});

export const append_block = tool({
  name: 'append_block',
  description: 'Append a new block to the end of a Notion page',
  parameters: z.object({
    page_id: z.string().describe('The Notion page ID to append to'),
    block_content: z.string().describe('The content to append as a new block'),
    block_type: z.enum(['paragraph', 'heading_1', 'heading_2', 'heading_3', 'bulleted_list_item', 'numbered_list_item']).describe('The type of block to create, usually paragraph'),
  }),
  execute: async ({ page_id, block_content, block_type }) => {
    try {
      const rich_text = [{ type: 'text' as const, text: { content: block_content } }];
      await notion.blocks.children.append({
        block_id: page_id,
        children: [
          { type: block_type, [block_type]: { rich_text } } as unknown as BlockObjectRequest
        ]
      });
      
      return {
        success: true,
        message: `Successfully appended block to page ${page_id}`
      };
    } catch (error) {
      throw new Error(`Failed to append block: ${error}`);
    }
  }
});

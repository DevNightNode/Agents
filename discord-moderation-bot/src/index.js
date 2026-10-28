import { Client, GatewayIntentBits } from 'discord.js';
import { ChatOpenAI } from '@langchain/openai';
import { createReactAgent } from '@langchain/langgraph/prebuilt';
import { tool } from '@langchain/core/tools';
import { z } from 'zod';
import { deleteMessage, timeoutMember, banMember, logAction } from './tools.js';

// Initialize Discord client
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildMembers
  ]
});

// LLM Configuration
const llm = new ChatOpenAI({
  modelName: 'gpt-4o',
  temperature: 0,
  openAIApiKey: process.env.OPENAI_API_KEY
});

// Define tools
const tools = [
  tool(async ({ messageId, channelId, guildId }) => {
    return await deleteMessage(messageId, channelId, guildId);
  }, {
    name: 'delete_message',
    description: 'Deletes a message from a Discord channel',
    schema: z.object({
      messageId: z.string().describe('The ID of the message to delete'),
      channelId: z.string().describe('The ID of the channel where the message is located'),
      guildId: z.string().describe('The ID of the guild where the message is located')
    })
  }),
  tool(async ({ memberId, guildId, duration, reason }) => {
    return await timeoutMember(memberId, guildId, duration, reason);
  }, {
    name: 'timeout_member',
    description: 'Timeouts a member in a Discord guild for a specified duration',
    schema: z.object({
      memberId: z.string().describe('The ID of the member to timeout'),
      guildId: z.string().describe('The ID of the guild where the member is located'),
      duration: z.number().describe('Timeout duration in seconds'),
      reason: z.string().describe('Reason for the timeout')
    })
  }),
  tool(async ({ memberId, guildId, reason }) => {
    return await banMember(memberId, guildId, reason);
  }, {
    name: 'ban_member',
    description: 'Bans a member from a Discord guild',
    schema: z.object({
      memberId: z.string().describe('The ID of the member to ban'),
      guildId: z.string().describe('The ID of the guild where the member is located'),
      reason: z.string().describe('Reason for the ban')
    })
  }),
  tool(async ({ action, details }) => {
    return await logAction(action, details);
  }, {
    name: 'log_action',
    description: 'Logs moderation actions to a database or file',
    schema: z.object({
      action: z.string().describe('Type of action performed (e.g., "delete", "timeout", "ban")'),
      details: z.object({
        messageId: z.string().optional().describe('ID of the message if applicable'),
        memberId: z.string().optional().describe('ID of the member if applicable'),
        guildId: z.string().optional().describe('ID of the guild if applicable'),
        reason: z.string().optional().describe('Reason for the action'),
        duration: z.number().optional().describe('Duration of timeout if applicable')
      }).describe('Details about the action')
    })
  })
];

// Create agent
const prompt = `You are a Discord moderation agent. Your job is to analyze messages and take appropriate moderation actions.
When a message violates Discord rules, you should:
1. Delete the message
2. Take appropriate action (timeout or ban) based on severity
3. Log the action

You have access to these tools:
- delete_message: Delete a message from a Discord channel
- timeout_member: Timeout a member for a specified duration
- ban_member: Ban a member from the guild
- log_action: Log moderation actions

Always respond with a JSON object containing the action you want to take.
If you want to take multiple actions, include all of them in the response.
`;

const agent = createReactAgent({
  llm,
  tools,
  prompt
});

// Handle message events
client.on('messageCreate', async (message) => {
  // Ignore bot messages
  if (message.author.bot) return;

  // Get guild and channel information
  const guild = message.guild;
  const channel = message.channel;

  if (!guild || !channel) return;

  // Analyze message with agent
  try {
    const result = await agent.invoke({
      messages: [{
        role: 'user',
        content: `Analyze this message for moderation violations: "${message.content}"\n\nChannel: ${channel.name} (${channel.id})\nGuild: ${guild.name} (${guild.id})\nAuthor: ${message.author.tag} (${message.author.id})`
      }]
    }, { recursionLimit: 20 });

    // Process the agent's response
    if (result.messages && result.messages.length > 0) {
      const response = result.messages[result.messages.length - 1];
      if (response.content) {
        console.log('Agent response:', response.content);
      }
    }
  } catch (error) {
    console.error('Error processing message:', error);
  }
});

// Handle member updates for moderation
client.on('guildMemberUpdate', async (oldMember, newMember) => {
  // Check if member was timed out
  if (oldMember.communicationDisabledUntil !== newMember.communicationDisabledUntil) {
    if (newMember.communicationDisabledUntil) {
      console.log(`Member ${newMember.user.tag} was timed out`);
    }
  }
});

// Login to Discord
client.login(process.env.DISCORD_BOT_TOKEN);

import { REST, Routes } from 'discord.js';
import fs from 'fs/promises';
import path from 'path';

const rest = new REST({ version: '10' }).setToken(process.env.DISCORD_BOT_TOKEN);

// Delete message from Discord
export async function deleteMessage(messageId, channelId, guildId) {
  try {
    await rest.delete(Routes.channelMessage(channelId, messageId));
    return { success: true, messageId, channelId, guildId };
  } catch (error) {
    console.error('Error deleting message:', error);
    throw error;
  }
}

// Timeout member in Discord
export async function timeoutMember(memberId, guildId, duration, reason) {
  try {
    const until = new Date(Date.now() + duration * 1000).toISOString();
    await rest.patch(Routes.guildMember(guildId, memberId), {
      body: { communication_disabled_until: until },
      reason,
    });
    return { success: true, memberId, guildId, duration, reason, until };
  } catch (error) {
    console.error('Error timing out member:', error);
    throw error;
  }
}

// Ban member from Discord
export async function banMember(memberId, guildId, reason) {
  try {
    await rest.put(Routes.guildBan(guildId, memberId), {
      body: { delete_message_seconds: 86400 },
      reason,
    });
    return { success: true, memberId, guildId, reason };
  } catch (error) {
    console.error('Error banning member:', error);
    throw error;
  }
}

// Log action to file
export async function logAction(action, details) {
  try {
    const logEntry = {
      timestamp: new Date().toISOString(),
      action,
      details
    };

    const logPath = path.join(process.cwd(), 'moderation.log');
    await fs.appendFile(logPath, JSON.stringify(logEntry) + '\n');
    console.log('Logged action:', logEntry);
    return { success: true, logEntry };
  } catch (error) {
    console.error('Error logging action:', error);
    throw error;
  }
}

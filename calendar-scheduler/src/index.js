import { ChatOpenAI } from '@langchain/openai';
import { createReactAgent } from '@langchain/langgraph/prebuilt';
import { tool } from '@langchain/core/tools';
import { z } from 'zod';
import { google } from 'googleapis';
import dotenv from 'dotenv';

dotenv.config();

// Service account with domain-wide delegation, acting as the scheduling user
const auth = new google.auth.GoogleAuth({
  keyFile: process.env.GOOGLE_APPLICATION_CREDENTIALS,
  scopes: ['https://www.googleapis.com/auth/calendar'],
  clientOptions: { subject: process.env.GOOGLE_CALENDAR_USER },
});
const calendar = google.calendar({ version: 'v3', auth });

const findFreeSlotsTool = tool(
  async ({ start_time, end_time, duration_minutes, attendees }) => {
    const calendarId = 'primary';
    const timeMin = new Date(start_time).toISOString();
    const timeMax = new Date(end_time).toISOString();
    const eventDuration = duration_minutes * 60 * 1000;

    const freeBusyRequest = {
      timeMin,
      timeMax,
      items: attendees.map(email => ({ id: email })),
    };

    const response = await calendar.freebusy.query({ requestBody: freeBusyRequest });
    const busySlots = response.data.calendars || {};

    const busyTimes = [];
    for (const [email, calendarData] of Object.entries(busySlots)) {
      if (calendarData.busy) {
        calendarData.busy.forEach(slot => {
          busyTimes.push({
            start: new Date(slot.start),
            end: new Date(slot.end),
          });
        });
      }
    }

    const freeSlots = [];
    const startTime = new Date(start_time);
    const endTime = new Date(end_time);

    let currentSlotStart = startTime;
    while (currentSlotStart < endTime) {
      const slotEnd = new Date(currentSlotStart.getTime() + eventDuration);
      if (slotEnd > endTime) break;

      let isFree = true;
      for (const busySlot of busyTimes) {
        if (
          (currentSlotStart >= busySlot.start && currentSlotStart < busySlot.end) ||
          (slotEnd > busySlot.start && slotEnd <= busySlot.end) ||
          (currentSlotStart <= busySlot.start && slotEnd >= busySlot.end)
        ) {
          isFree = false;
          currentSlotStart = busySlot.end;
          break;
        }
      }

      if (isFree) {
        freeSlots.push({
          start: currentSlotStart.toISOString(),
          end: slotEnd.toISOString(),
        });
        currentSlotStart = slotEnd;
      }
    }

    return freeSlots;
  },
  {
    name: 'find_free_slots',
    description: 'Find free time slots for a meeting given time constraints and attendees',
    schema: z.object({
      start_time: z.string().describe('Start time in ISO format'),
      end_time: z.string().describe('End time in ISO format'),
      duration_minutes: z.number().describe('Meeting duration in minutes'),
      attendees: z.array(z.string()).describe('List of attendee email addresses'),
    }),
  }
);

const createEventTool = tool(
  async ({ summary, start_time, end_time, attendees, description, location }) => {
    const calendarId = 'primary';
    const event = {
      summary,
      description,
      location,
      start: {
        dateTime: new Date(start_time).toISOString(),
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      },
      end: {
        dateTime: new Date(end_time).toISOString(),
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      },
      attendees: attendees.map(email => ({ email })),
      reminders: {
        useDefault: true,
      },
    };

    const response = await calendar.events.insert({
      calendarId,
      requestBody: event,
    });

    return {
      event_id: response.data.id,
      link: response.data.htmlLink,
      summary: response.data.summary,
      start: response.data.start.dateTime,
      end: response.data.end.dateTime,
    };
  },
  {
    name: 'create_event',
    description: 'Create a new calendar event with specified details',
    schema: z.object({
      summary: z.string().describe('Event title'),
      start_time: z.string().describe('Start time in ISO format'),
      end_time: z.string().describe('End time in ISO format'),
      attendees: z.array(z.string()).describe('List of attendee email addresses'),
      description: z.string().optional().describe('Event description'),
      location: z.string().optional().describe('Event location'),
    }),
  }
);

const cancelEventTool = tool(
  async ({ event_id }) => {
    const calendarId = 'primary';
    await calendar.events.delete({
      calendarId,
      eventId: event_id,
    });

    return { message: `Event ${event_id} has been cancelled successfully` };
  },
  {
    name: 'cancel_event',
    description: 'Cancel an existing calendar event by event ID',
    schema: z.object({
      event_id: z.string().describe('The ID of the event to cancel'),
    }),
  }
);

const llm = new ChatOpenAI({
  model: 'gpt-4-turbo',
  temperature: 0,
});

const tools = [
  findFreeSlotsTool,
  createEventTool,
  cancelEventTool,
];

const systemPrompt = `
You are a calendar scheduling assistant. You help users find free time slots, create meetings, and cancel existing meetings.
Always use the appropriate tool for each request:
- Use find_free_slots when users ask to find available time slots
- Use create_event when users want to schedule a new meeting
- Use cancel_event when users want to cancel an existing meeting

Be precise with time formats and always confirm event details before taking action.
`;

const agent = createReactAgent({
  llm,
  tools,
  prompt: systemPrompt,
});

async function main() {
  const userInput = process.argv[2] || 'Find me a free slot for a 60-minute meeting with john@example.com and jane@example.com between 2023-10-01T09:00:00Z and 2023-10-01T17:00:00Z';
  const result = await agent.invoke({ messages: [{ role: 'user', content: userInput }] }, { recursionLimit: 20 });
  console.log('Agent response:', JSON.stringify(result.messages[0].content, null, 2));
}

if (process.argv[1] === new URL(import.meta.url).pathname) {
  main();
}

export { agent, findFreeSlotsTool, createEventTool, cancelEventTool };

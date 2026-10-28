import { generateText, tool } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';
import pg from 'pg';
import twilio from 'twilio';

// Reservations live in the restaurant's Postgres database:
//   reservation(id serial, starts_at timestamptz, party_size int, customer_name text, customer_phone text)
const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });
const twilioClient = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);

const SEAT_CAPACITY = Number(process.env.SEAT_CAPACITY ?? 60);
const SITTING_MINUTES = 90;

// Seats already booked in sittings that overlap a 90-minute window starting at `startsAt`
async function bookedSeats(startsAt) {
  const { rows } = await pool.query(
    `SELECT COALESCE(SUM(party_size), 0)::int AS seats
       FROM reservation
      WHERE starts_at > $1::timestamptz - make_interval(mins => $2)
        AND starts_at < $1::timestamptz + make_interval(mins => $2)`,
    [startsAt, SITTING_MINUTES]
  );
  return rows[0].seats;
}

// Tool to check restaurant availability
const checkAvailability = tool({
  description: 'Check if a table is available for a given date and time',
  parameters: z.object({
    date: z.string().describe('Date in YYYY-MM-DD format'),
    time: z.string().describe('Time in HH:MM format'),
    partySize: z.number().describe('Number of people in the party')
  }),
  execute: async ({ date, time, partySize }) => {
    const seats = await bookedSeats(`${date} ${time}`);
    const available = seats + partySize <= SEAT_CAPACITY;
    return {
      available,
      message: available
        ? `Table available for ${partySize} people on ${date} at ${time}`
        : `No table available for ${partySize} people on ${date} at ${time}`
    };
  }
});

// Tool to book a table
const bookTable = tool({
  description: 'Book a table for a given date and time',
  parameters: z.object({
    date: z.string().describe('Date in YYYY-MM-DD format'),
    time: z.string().describe('Time in HH:MM format'),
    partySize: z.number().describe('Number of people in the party'),
    customerName: z.string().describe('Name of the customer'),
    customerPhone: z.string().describe('Phone number of the customer')
  }),
  execute: async ({ date, time, partySize, customerName, customerPhone }) => {
    const startsAt = `${date} ${time}`;
    if ((await bookedSeats(startsAt)) + partySize > SEAT_CAPACITY) {
      return { booked: false, message: `Sorry, ${date} at ${time} is now fully booked` };
    }
    const { rows } = await pool.query(
      `INSERT INTO reservation (starts_at, party_size, customer_name, customer_phone)
       VALUES ($1, $2, $3, $4) RETURNING id`,
      [startsAt, partySize, customerName, customerPhone]
    );
    const bookingId = rows[0].id;
    const confirmation = `Booking confirmed! Table for ${partySize} people on ${date} at ${time} for ${customerName}. Booking ID: ${bookingId}`;
    return {
      booked: true,
      bookingId,
      confirmation,
      message: confirmation
    };
  }
});

// Tool to send SMS
const sendSms = tool({
  description: 'Send an SMS message to a phone number',
  parameters: z.object({
    to: z.string().describe('Phone number to send SMS to'),
    message: z.string().describe('Message content')
  }),
  execute: async ({ to, message }) => {
    const sent = await twilioClient.messages.create({
      from: process.env.TWILIO_PHONE_NUMBER,
      to,
      body: message
    });
    return {
      success: true,
      sid: sent.sid,
      message: `SMS sent to ${to}`
    };
  }
});

// Agent system instructions
const systemPrompt = `
You are a restaurant reservation concierge assistant. You help customers book tables by checking availability and making reservations.
Always ask for the date, time, party size, and customer details before booking.
Use the available tools to check availability, book tables, and send SMS confirmations.
Keep responses concise and friendly.
`;

// Main agent function
export async function processSmsMessage(message, customerPhone) {
  const result = await generateText({
    model: openai('gpt-4.1'),
    system: `${systemPrompt}\nThe customer is texting from ${customerPhone}.`,
    prompt: message,
    tools: {
      checkAvailability,
      bookTable,
      sendSms
    },
    maxSteps: 8
  });

  return result;
}

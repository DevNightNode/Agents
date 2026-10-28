import express from 'express';
import { processSmsMessage } from './agent.js';
import twilio from 'twilio';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

// Middleware to parse JSON and URL-encoded data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Twilio webhook endpoint
app.post('/webhook', async (req, res) => {
  try {
    const incomingMessage = req.body.Body;
    const customerPhone = req.body.From;

    console.log(`Received SMS from ${customerPhone}: ${incomingMessage}`);

    // Process the SMS message with the AI agent
    const result = await processSmsMessage(incomingMessage, customerPhone);

    // Send the response back via SMS
    const twilioClient = twilio(
      process.env.TWILIO_ACCOUNT_SID,
      process.env.TWILIO_AUTH_TOKEN
    );

    await twilioClient.messages.create({
      body: result.text,
      from: process.env.TWILIO_PHONE_NUMBER,
      to: customerPhone
    });

    res.status(200).send('Message processed');
  } catch (error) {
    console.error('Error processing SMS:', error);
    res.status(500).send('Error processing message');
  }
});

app.listen(port, () => {
  console.log(`Twilio SMS Concierge server running on port ${port}`);
});

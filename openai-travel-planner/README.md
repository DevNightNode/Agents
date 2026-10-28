# OpenAI Travel Planner

An AI-powered travel planning agent that helps users search and book flights and hotels using the Amadeus API.

## Features

- **Triage Agent**: Determines whether a user wants to book flights or hotels
- **Flight Agent**: Searches for and books flights
- **Hotel Agent**: Searches for and books hotels
- **Secure Payment**: Pays for hotel bookings with a company card from the environment
- **Input Guardrail**: Prevents sensitive information in user input

## Tools

1. `search_flights(origin, destination, departure_date, return_date=None, travelers=1, max_price=None)`
   - Search for flights between origin and destination
   - Supports round-trip flights, multiple travelers, and price filtering

2. `search_hotels(destination, checkin_date, checkout_date, guests=1, max_price=None)`
   - Search for hotels in a destination
   - Supports date ranges, guest count, and price filtering

3. `book_flight(flight_offer_json, first_name, last_name, date_of_birth, gender, email, phone_country_code, phone_number)`
   - Creates an Amadeus flight order for an offer returned by `search_flights`

4. `book_hotel(offer_id, title, first_name, last_name, email, phone)`
   - Book a hotel using Amadeus API
   - Pays with the company card (PAYMENT_CARD_* env vars)

## Required Environment Variables

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
AMADEUS_CLIENT_ID=your_amadeus_client_id_here
AMADEUS_CLIENT_SECRET=your_amadeus_client_secret_here
PAYMENT_CARD_VENDOR=VI
PAYMENT_CARD_NUMBER=4111111111111111
PAYMENT_CARD_EXPIRY=2030-01
```

## Running

```bash
pip install -r requirements.txt
python main.py
```

The triage agent hands flight requests to the flight agent and hotel requests to the hotel agent. An input guardrail rejects messages that paste passwords or card details.

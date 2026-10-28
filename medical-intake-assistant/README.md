# Medical Intake Assistant

A LangGraph-based chatbot that collects patient symptoms, looks up patient records in a FHIR server, and books appointments.

## Overview

The Medical Intake Assistant is an intelligent chatbot designed to streamline clinic intake processes. It collects patient symptoms, retrieves patient information from a FHIR server, and facilitates appointment booking with available slots.

## Tools

### 1. lookup_patient
- **Purpose**: Look up patient information in the FHIR server
- **Parameters**:
  - `patient_id` (str): The FHIR patient ID to look up
- **Returns**: Patient information including name, birth date, gender, and contact details

### 2. get_available_slots
- **Purpose**: Get available appointment slots for a given date
- **Parameters**:
  - `date` (str): The date to check for available slots (format: YYYY-MM-DD)
  - `practitioner_id` (str, optional): Specific practitioner ID to check slots for
- **Returns**: List of available time slots with start and end times

### 3. book_appointment
- **Purpose**: Book an appointment for a patient with a practitioner
- **Parameters**:
  - `patient_id` (str): The FHIR patient ID
  - `practitioner_id` (str): The FHIR practitioner ID
  - `start_time` (str): Appointment start time (ISO format)
  - `end_time` (str): Appointment end time (ISO format)
  - `reason` (str): Reason for the appointment
- **Returns**: Appointment booking confirmation details

## Required Environment Variables

Create a `.env` file with the following variables:

```
OPENAI_API_KEY=your_openai_api_key_here
FHIR_SERVER_URL=https://your-fhir-server.com/fhir
FHIR_API_KEY=your_fhir_api_key_here
```

## How to Run

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env` file

3. Run the assistant:
   ```
   python main.py
   ```

4. Interact with the assistant by typing patient information and appointment requests

## Features

- Natural language conversation with patient
- FHIR server integration for patient records
- Appointment slot availability checking
- Appointment booking functionality
- Error handling for API failures
- Conversation state management

## Requirements

- Python 3.8+
- OpenAI API key
- FHIR server with REST API access
- Network connectivity to FHIR server

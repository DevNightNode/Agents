# Invoice OCR Processor

An AI-powered accounts payable agent that processes PDF invoices using OCR, extracts key fields, matches purchase orders in an ERP system, and schedules payments.

## Features

This agent automates the accounts payable workflow by:
1. Extracting invoice details from PDFs using OCR
2. Matching extracted invoices against purchase orders in the ERP database
3. Scheduling payments for valid invoices

## Tools

### 1. `extract_invoice`
- **Purpose**: Extract structured invoice data from PDF files
- **Input**: PDF file path
- **Output**: JSON object with fields: invoice_number, vendor_name, vendor_address, invoice_date, due_date, total_amount, currency, po_number
- **Implementation**: Uses pdfplumber for OCR and OpenAI GPT-4 to parse structured data

### 2. `match_purchase_order`
- **Purpose**: Verify that a purchase order exists in the ERP system
- **Input**: PO number, vendor name, total amount
- **Output**: JSON object with PO details if found, or error message
- **Implementation**: Queries MySQL database for matching PO records

### 3. `schedule_payment`
- **Purpose**: Schedule payment in the ERP system
- **Input**: Vendor name, payment amount, due date, PO number
- **Output**: Confirmation message with payment ID
- **Implementation**: Inserts payment schedule into MySQL database

## Required Environment Variables

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
DB_HOST=localhost
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env` file

3. Run the agent:
```bash
python main.py
```

## Usage

The agent can be invoked with natural language commands like:
- "Process invoice from vendor Acme Corp for $1500.00 due 2023-10-15"
- "Extract invoice details from invoice.pdf and match against PO 12345"
- "Schedule payment for invoice #INV-001 for $2500.00"

The agent will automatically chain the appropriate tools to complete the requested task.

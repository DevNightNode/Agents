import os
import re
from typing import Optional
from pydantic_ai import RunContext

# Import required libraries
import pdfplumber
import pymysql
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Database connection
def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        charset='utf8mb4'
    )

async def extract_invoice(ctx: RunContext, pdf_path: str) -> str:
    """
    Extract invoice details from a PDF file using OCR.
    
    Args:
        pdf_path (str): Path to the PDF invoice file
        
    Returns:
        str: JSON string containing extracted invoice details
    """
    try:
        # Extract text from PDF
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        # Use OpenAI to parse structured data from extracted text
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Extract the following fields from the invoice text: invoice_number, vendor_name, vendor_address, invoice_date, due_date, total_amount, currency, po_number. Return a JSON object with these fields. If any field is not found, set it to null."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            response_format={"type": "json_object"}
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error extracting invoice: {str(e)}"

async def match_purchase_order(ctx: RunContext, po_number: str, vendor_name: str, total_amount: float) -> str:
    """
    Match a purchase order in the ERP database based on PO number, vendor, and amount.
    
    Args:
        po_number (str): Purchase order number
        vendor_name (str): Vendor name
        total_amount (float): Total invoice amount
        
    Returns:
        str: JSON string containing matching PO details or error message
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        # Query for matching PO
        query = """
        SELECT po_number, vendor_name, total_amount, status, created_date 
        FROM purchase_orders 
        WHERE po_number = %s AND vendor_name = %s AND ABS(total_amount - %s) < 0.01
        """
        cursor.execute(query, (po_number, vendor_name, total_amount))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            return f"PO matched: {result}"
        else:
            return "No matching PO found in ERP database"
            
    except Exception as e:
        return f"Error matching PO: {str(e)}"

async def schedule_payment(ctx: RunContext, vendor_name: str, total_amount: float, due_date: str, po_number: str) -> str:
    """
    Schedule payment for an invoice in the ERP system.
    
    Args:
        vendor_name (str): Vendor name
        total_amount (float): Payment amount
        due_date (str): Payment due date
        po_number (str): Purchase order number
        
    Returns:
        str: Confirmation message with payment details
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        # Insert payment schedule
        query = """
        INSERT INTO payment_schedules (vendor_name, amount, due_date, po_number, status, created_date)
        VALUES (%s, %s, %s, %s, 'scheduled', NOW())
        """
        cursor.execute(query, (vendor_name, total_amount, due_date, po_number))
        conn.commit()
        
        payment_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        return f"Payment scheduled successfully. Payment ID: {payment_id}"
        
    except Exception as e:
        return f"Error scheduling payment: {str(e)}"

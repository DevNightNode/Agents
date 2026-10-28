import os
import requests
from typing import Optional, List, Dict, Any
from langchain_core.tools import tool
from datetime import datetime

# FHIR server configuration
FHIR_BASE_URL = os.getenv("FHIR_SERVER_URL")
FHIR_API_KEY = os.getenv("FHIR_API_KEY")

def _fhir_request(endpoint: str, method: str = "GET", data: Optional[Dict] = None,
                  params: Optional[Any] = None) -> Dict:
    """Make a request to the FHIR server."""
    headers = {
        "Authorization": f"Bearer {FHIR_API_KEY}",
        "Content-Type": "application/fhir+json",
        "Accept": "application/fhir+json"
    }
    
    url = f"{FHIR_BASE_URL}/{endpoint}"
    
    if method == "GET":
        response = requests.get(url, headers=headers, params=params)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=data)
    elif method == "PUT":
        response = requests.put(url, headers=headers, json=data)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")
    
    response.raise_for_status()
    return response.json()

@tool
def lookup_patient(patient_id: str) -> Dict[str, Any]:
    """
    Look up patient information in the FHIR server.
    
    Args:
        patient_id (str): The FHIR patient ID to look up
        
    Returns:
        Dict containing patient information including name, birth date, and contact details
    """
    try:
        patient_data = _fhir_request(f"Patient/{patient_id}")
        return {
            "id": patient_data.get("id"),
            "name": patient_data.get("name", [{}])[0].get("given", ["Unknown"])[0] + " " + patient_data.get("name", [{}])[0].get("family", "Unknown"),
            "birth_date": patient_data.get("birthDate"),
            "gender": patient_data.get("gender"),
            "telecom": patient_data.get("telecom", []),
            "address": patient_data.get("address", [{}])[0]
        }
    except Exception as e:
        return {"error": f"Failed to lookup patient: {str(e)}"}

@tool
def get_available_slots(date: str, practitioner_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get available appointment slots for a given date.
    
    Args:
        date (str): The date to check for available slots (format: YYYY-MM-DD)
        practitioner_id (str, optional): Specific practitioner ID to check slots for
        
    Returns:
        List of available time slots with start and end times
    """
    try:
        # Free Slot resources starting on that day
        params = [("status", "free"), ("start", f"ge{date}T00:00:00"), ("start", f"lt{date}T23:59:59")]
        if practitioner_id:
            params.append(("schedule.actor", f"Practitioner/{practitioner_id}"))

        response_data = _fhir_request("Slot", "GET", params=params)

        slots = []
        for entry in response_data.get("entry", []):
            slot = entry.get("resource", {})
            slots.append({
                "slot_id": slot.get("id"),
                "start": slot.get("start"),
                "end": slot.get("end"),
                "schedule": slot.get("schedule", {}).get("reference", "Unknown")
            })

        return slots
    except Exception as e:
        return [{"error": f"Failed to get available slots: {str(e)}"}]

@tool
def book_appointment(
    patient_id: str,
    practitioner_id: str,
    start_time: str,
    end_time: str,
    reason: str
) -> Dict[str, Any]:
    """
    Book an appointment for a patient with a practitioner.
    
    Args:
        patient_id (str): The FHIR patient ID
        practitioner_id (str): The FHIR practitioner ID
        start_time (str): Appointment start time (ISO format)
        end_time (str): Appointment end time (ISO format)
        reason (str): Reason for the appointment
        
    Returns:
        Dict containing appointment booking confirmation details
    """
    try:
        # Create appointment resource
        appointment_data = {
            "resourceType": "Appointment",
            "status": "booked",
            "start": start_time,
            "end": end_time,
            "participant": [
                {
                    "actor": {
                        "reference": f"Patient/{patient_id}"
                    },
                    "status": "accepted"
                },
                {
                    "actor": {
                        "reference": f"Practitioner/{practitioner_id}"
                    },
                    "status": "accepted"
                }
            ],
            "description": reason
        }
        
        # Create the appointment
        response = _fhir_request("Appointment", "POST", appointment_data)
        
        return {
            "id": response.get("id"),
            "status": "booked",
            "patient_id": patient_id,
            "practitioner_id": practitioner_id,
            "start_time": start_time,
            "end_time": end_time,
            "reason": reason
        }
    except Exception as e:
        return {"error": f"Failed to book appointment: {str(e)}"}

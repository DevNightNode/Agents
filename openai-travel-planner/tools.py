import json
import os
import requests
from typing import Optional, List, Dict, Any
from agents import function_tool

# Amadeus API credentials from environment variables
AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")
AMADEUS_API_URL = "https://test.api.amadeus.com"

# Company card used for hotel payments
PAYMENT_CARD_VENDOR = os.getenv("PAYMENT_CARD_VENDOR")  # e.g. VI, CA, AX
PAYMENT_CARD_NUMBER = os.getenv("PAYMENT_CARD_NUMBER")
PAYMENT_CARD_EXPIRY = os.getenv("PAYMENT_CARD_EXPIRY")  # YYYY-MM

class AmadeusAPIError(Exception):
    """Custom exception for Amadeus API errors"""
    pass

def _get_amadeus_token() -> str:
    """Get access token from Amadeus API"""
    if not AMADEUS_CLIENT_ID or not AMADEUS_CLIENT_SECRET:
        raise AmadeusAPIError("AMADEUS_CLIENT_ID and AMADEUS_CLIENT_SECRET must be set")
    
    response = requests.post(
        f"{AMADEUS_API_URL}/v1/security/oauth2/token",
        data={
            "grant_type": "client_credentials",
            "client_id": AMADEUS_CLIENT_ID,
            "client_secret": AMADEUS_CLIENT_SECRET
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if response.status_code != 200:
        raise AmadeusAPIError(f"Failed to get Amadeus token: {response.text}")
    
    return response.json()["access_token"]

@function_tool
def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: Optional[str] = None,
    travelers: int = 1,
    max_price: Optional[int] = None
) -> Dict[str, Any]:
    """
    Search for flights between origin and destination.
    
    Args:
        origin: Origin airport code (e.g., 'JFK')
        destination: Destination airport code (e.g., 'LAX')
        departure_date: Departure date in YYYY-MM-DD format
        return_date: Return date in YYYY-MM-DD format (optional)
        travelers: Number of travelers (default: 1)
        max_price: Maximum price in USD (optional)
    
    Returns:
        Dictionary containing flight search results
    """
    try:
        token = _get_amadeus_token()
        
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "adults": travelers,
            "max": 10
        }
        
        if return_date:
            params["returnDate"] = return_date
            
        if max_price:
            params["maxPrice"] = max_price
            
        response = requests.get(
            f"{AMADEUS_API_URL}/v2/shopping/flight-offers",
            params=params,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code != 200:
            raise AmadeusAPIError(f"Flight search failed: {response.text}")
            
        return response.json()
        
    except Exception as e:
        raise AmadeusAPIError(f"Error searching flights: {str(e)}")

@function_tool
def search_hotels(
    destination: str,
    checkin_date: str,
    checkout_date: str,
    guests: int = 1,
    max_price: Optional[int] = None
) -> Dict[str, Any]:
    """
    Search for hotels in a destination.
    
    Args:
        destination: Destination city or airport code (e.g., 'PAR')
        checkin_date: Check-in date in YYYY-MM-DD format
        checkout_date: Check-out date in YYYY-MM-DD format
        guests: Number of guests (default: 1)
        max_price: Maximum price per night in USD (optional)
    
    Returns:
        Dictionary containing hotel search results
    """
    try:
        token = _get_amadeus_token()
        
        params = {
            "cityCode": destination,
            "checkInDate": checkin_date,
            "checkOutDate": checkout_date,
            "adults": guests,
            "max": 10
        }
        
        if max_price:
            params["maxPrice"] = max_price
            
        response = requests.get(
            f"{AMADEUS_API_URL}/shopping/hotel-offers",
            params=params,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code != 200:
            raise AmadeusAPIError(f"Hotel search failed: {response.text}")
            
        return response.json()
        
    except Exception as e:
        raise AmadeusAPIError(f"Error searching hotels: {str(e)}")

@function_tool
def book_flight(
    flight_offer_json: str,
    first_name: str,
    last_name: str,
    date_of_birth: str,
    gender: str,
    email: str,
    phone_country_code: str,
    phone_number: str
) -> Dict[str, Any]:
    """
    Book a flight offer with the Amadeus Flight Create Orders API.

    Args:
        flight_offer_json: The exact flight offer object returned by search_flights, as a JSON string
        first_name: Traveler's first name as on their passport
        last_name: Traveler's last name as on their passport
        date_of_birth: Traveler's date of birth, YYYY-MM-DD
        gender: MALE or FEMALE, as on the passport
        email: Traveler's email address
        phone_country_code: Phone country calling code without +, e.g. 1
        phone_number: Phone number without the country code

    Returns:
        The created flight order, including its booking reference
    """
    try:
        token = _get_amadeus_token()

        booking_data = {
            "data": {
                "type": "flight-order",
                "flightOffers": [json.loads(flight_offer_json)],
                "travelers": [
                    {
                        "id": "1",
                        "dateOfBirth": date_of_birth,
                        "name": {"firstName": first_name, "lastName": last_name},
                        "gender": gender,
                        "contact": {
                            "emailAddress": email,
                            "phones": [{
                                "deviceType": "MOBILE",
                                "countryCallingCode": phone_country_code,
                                "number": phone_number
                            }]
                        }
                    }
                ]
            }
        }

        response = requests.post(
            f"{AMADEUS_API_URL}/v1/booking/flight-orders",
            json=booking_data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/vnd.amadeus+json"
            }
        )

        if response.status_code != 201:
            raise AmadeusAPIError(f"Flight booking failed: {response.text}")

        return response.json()

    except Exception as e:
        raise AmadeusAPIError(f"Error booking flight: {str(e)}")

@function_tool
def book_hotel(
    offer_id: str,
    title: str,
    first_name: str,
    last_name: str,
    email: str,
    phone: str
) -> Dict[str, Any]:
    """
    Book a hotel offer with the Amadeus Hotel Booking API, paying with the company card.

    Args:
        offer_id: The offer ID returned by search_hotels
        title: Guest title, e.g. MR, MS, MRS
        first_name: Guest's first name
        last_name: Guest's last name
        email: Guest's email address
        phone: Guest's phone number in international format, e.g. +15555550123

    Returns:
        Booking confirmation details
    """
    try:
        if not (PAYMENT_CARD_NUMBER and PAYMENT_CARD_EXPIRY and PAYMENT_CARD_VENDOR):
            raise AmadeusAPIError("PAYMENT_CARD_VENDOR, PAYMENT_CARD_NUMBER and PAYMENT_CARD_EXPIRY must be set to book hotels")

        token = _get_amadeus_token()

        booking_data = {
            "data": {
                "offerId": offer_id,
                "guests": [
                    {
                        "id": 1,
                        "name": {"title": title, "firstName": first_name, "lastName": last_name},
                        "contact": {"phone": phone, "email": email}
                    }
                ],
                "payments": [
                    {
                        "id": 1,
                        "method": "creditCard",
                        "card": {
                            "vendorCode": PAYMENT_CARD_VENDOR,
                            "cardNumber": PAYMENT_CARD_NUMBER,
                            "expiryDate": PAYMENT_CARD_EXPIRY
                        }
                    }
                ]
            }
        }

        response = requests.post(
            f"{AMADEUS_API_URL}/v1/booking/hotel-bookings",
            json=booking_data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/vnd.amadeus+json"
            }
        )

        if response.status_code != 201:
            raise AmadeusAPIError(f"Hotel booking failed: {response.text}")

        return response.json()

    except Exception as e:
        raise AmadeusAPIError(f"Error booking hotel: {str(e)}")

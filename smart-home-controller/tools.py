import os
import requests
from typing import Optional, Dict, Any
from agents import function_tool

# Home Assistant configuration from environment variables
HA_URL = os.environ.get("HOME_ASSISTANT_URL")
HA_TOKEN = os.environ.get("HOME_ASSISTANT_TOKEN")

# Validate configuration
if not HA_URL or not HA_TOKEN:
    raise ValueError("HOME_ASSISTANT_URL and HOME_ASSISTANT_TOKEN must be set in environment")

# Headers for Home Assistant API requests
HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json"
}

@function_tool
def get_states() -> Dict[str, Any]:
    """
    Get the current state of all entities in Home Assistant.
    
    Returns:
        A dictionary containing all entity states with their attributes.
    """
    try:
        response = requests.get(f"{HA_URL}/api/states", headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch states from Home Assistant: {str(e)}")

@function_tool
def set_light(entity_id: str, brightness: Optional[int] = None, rgb_color: Optional[tuple] = None) -> str:
    """
    Control a light entity in Home Assistant.
    
    Args:
        entity_id: The entity ID of the light (e.g., 'light.living_room_light')
        brightness: The brightness level (0-255)
        rgb_color: The RGB color values as a tuple (r, g, b)
        
    Returns:
        A message confirming the action was taken.
    """
    try:
        data = {"entity_id": entity_id}
        
        if brightness is not None:
            data["brightness"] = brightness
            
        if rgb_color is not None:
            data["rgb_color"] = rgb_color
            
        response = requests.post(f"{HA_URL}/api/services/light/turn_on", 
                               headers=HEADERS, 
                               json=data)
        response.raise_for_status()
        return f"Successfully controlled light {entity_id}"
    except requests.RequestException as e:
        raise Exception(f"Failed to control light {entity_id}: {str(e)}")

@function_tool
def set_thermostat(entity_id: str, temperature: Optional[float] = None, 
                  hvac_mode: Optional[str] = None) -> str:
    """
    Control a thermostat entity in Home Assistant.
    
    Args:
        entity_id: The entity ID of the thermostat (e.g., 'climate.bedroom_thermostat')
        temperature: The target temperature
        hvac_mode: The HVAC mode (e.g., 'heat', 'cool', 'auto', 'off')
        
    Returns:
        A message confirming the action was taken.
    """
    try:
        data = {"entity_id": entity_id}
        
        if temperature is not None:
            data["temperature"] = temperature
            
        if hvac_mode is not None:
            data["hvac_mode"] = hvac_mode
            
        response = requests.post(f"{HA_URL}/api/services/climate/set_temperature", 
                               headers=HEADERS, 
                               json=data)
        response.raise_for_status()
        return f"Successfully controlled thermostat {entity_id}"
    except requests.RequestException as e:
        raise Exception(f"Failed to control thermostat {entity_id}: {str(e)}")

@function_tool
def unlock_door(entity_id: str) -> str:
    """
    Unlock a door lock entity in Home Assistant.
    
    Args:
        entity_id: The entity ID of the door lock (e.g., 'lock.front_door')
        
    Returns:
        A message confirming the action was taken.
    """
    try:
        data = {"entity_id": entity_id}
        response = requests.post(f"{HA_URL}/api/services/lock/unlock", 
                               headers=HEADERS, 
                               json=data)
        response.raise_for_status()
        return f"Successfully unlocked door {entity_id}"
    except requests.RequestException as e:
        raise Exception(f"Failed to unlock door {entity_id}: {str(e)}")

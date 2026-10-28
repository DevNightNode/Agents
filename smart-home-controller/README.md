# Smart Home Controller Agent

A Home Assistant agent that reads sensor states and controls lights, thermostats, and door locks via the REST API.

## Overview

This agent allows users to interact with their Home Assistant system through natural language commands. It can read the current state of all entities and control various smart home devices including lights, thermostats, and door locks.

## Tools

### 1. `get_states`
- **Description**: Retrieves the current state of all entities in Home Assistant
- **Usage**: Get information about all sensors, lights, thermostats, and other devices
- **Returns**: A dictionary containing all entity states with their attributes

### 2. `set_light`
- **Description**: Controls a light entity in Home Assistant
- **Parameters**:
  - `entity_id` (str): The entity ID of the light (e.g., 'light.living_room_light')
  - `brightness` (int, optional): The brightness level (0-255)
  - `rgb_color` (tuple, optional): The RGB color values as a tuple (r, g, b)
- **Usage**: Turn lights on/off, adjust brightness, or change colors

### 3. `set_thermostat`
- **Description**: Controls a thermostat entity in Home Assistant
- **Parameters**:
  - `entity_id` (str): The entity ID of the thermostat (e.g., 'climate.bedroom_thermostat')
  - `temperature` (float, optional): The target temperature
  - `hvac_mode` (str, optional): The HVAC mode (e.g., 'heat', 'cool', 'auto', 'off')
- **Usage**: Set temperature or change HVAC mode

### 4. `unlock_door`
- **Description**: Unlocks a door lock entity in Home Assistant
- **Parameters**:
  - `entity_id` (str): The entity ID of the door lock (e.g., 'lock.front_door')
- **Usage**: Unlock doors and gates

## Required Environment Variables

Create a `.env` file in the project root with the following variables:

```env
HOME_ASSISTANT_URL=https://your-home-assistant-url
HOME_ASSISTANT_TOKEN=your-long-lived-access-token
```

You can generate a long-lived access token in your Home Assistant profile settings.

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your environment variables in a `.env` file

3. Run the agent:
   ```bash
   python main.py
   ```

The agent will execute with a sample input. You can modify the `user_input` parameter in `main.py` to test different commands.

## Example Usage

```bash
python main.py
```

This will:
1. Connect to your Home Assistant instance
2. Get current states of all entities
3. Return the results to the user

You can also interact with the agent by modifying the `user_input` parameter to ask specific questions or commands.

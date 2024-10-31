# Smart Plug Controller GUI

This project is a Python-based graphical user interface (GUI) for controlling a smart plug and monitoring temperature and humidity using a DHT11 sensor. The GUI allows users to:

- Turn the smart plug on and off manually.
- Schedule times for turning the plug on and off automatically.
- Specify a desired temperature range.
- Monitor and display temperature and humidity.
- View energy consumption statistics of the smart plug (if supported).

## Requirements

To run this project, the following software and hardware are required:

### Software Requirements

- Python 3.7+
- CustomTkinter library for GUI (`customtkinter`)
- asyncio and threading modules (included in Python standard library)
- `kasa` library to control the TP-Link smart plug
- `Adafruit_DHT` library to interact with the DHT11 sensor
- pip to install dependencies

### Hardware Requirements

- TP-Link Smart Plug (e.g., HS110) with power monitoring capability
- DHT11 temperature and humidity sensor
- Raspberry Pi (or other device with GPIO capability for connecting the sensor)

## Installation

1. Clone the repository or download the project files.
2. Install the required Python packages using pip:

   ```bash
   pip install customtkinter python-kasa Adafruit_DHT
   ```
3. Update the `PLUG_IP` variable in the script with the IP address of your smart plug.
4. Connect the DHT11 sensor to the appropriate GPIO pin on your Raspberry Pi (or compatible device).

## Running the Application

To run the application, simply execute the Python script:

```bash
python gui.py
```

This will open the GUI window where you can interact with the smart plug and sensor data.

## Usage

- **Turn On/Off Buttons**: Use these buttons to manually turn the plug on or off.
- **Schedule On/Off**: Enter a specific time (in `HH:MM` format) to schedule the plug to turn on or off automatically.
- **Auto Mode**: Enter a temperature range and the fan would automatically keep the temperature in that range.
- **Energy Consumption Statistics**: Click the "Refresh Stats" button to view the power consumption statistics of the smart plug.

## Features

- **Manual Control**: Turn the plug on or off directly from the GUI.
- **Scheduling**: Schedule specific times to turn the plug on or off.
- **Temperature and Humidity Readings**: Monitor environmental data using the DHT11 sensor.
- **Energy Monitoring**: Display energy consumption statistics (if the smart plug supports energy monitoring).

## Notes

- Make sure the smart plug and the device running the script are on the same network.
- The DHT11 sensor needs proper GPIO configuration to work with the Raspberry Pi.
- Replace `PLUG_IP` with the correct IP address of your smart plug before running the script.

## License

This project is licensed under the MIT License. Feel free to modify and distribute it as needed.


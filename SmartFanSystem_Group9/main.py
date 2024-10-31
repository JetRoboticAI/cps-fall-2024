import asyncio
from datetime import datetime
import threading
import time
import customtkinter as ctk
from kasa import SmartPlug
from kasa.exceptions import KasaException

import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

# IP address of the smart plug
PLUG_IP = "192.168.0.188" 

# Global variables for storing the scheduled times
turn_on_time = None
turn_off_time = None

status = False

# Function to turn the plug on
async def turn_on_plug():
    plug = SmartPlug(PLUG_IP)
    await plug.update()
    try:
        await plug.turn_on()
        status = True
        print("Plug turned on.")
    except KasaException as e:
        print(f"Failed to turn on the plug: {e}")

# Function to turn the plug off
async def turn_off_plug():
    plug = SmartPlug(PLUG_IP)
    await plug.update()
    try:
        await plug.turn_off()
        status = False
        print("Plug turned off.")
    except KasaException as e:
        print(f"Failed to turn off the plug: {e}")

# Retry logic for the async functions
async def retry_async_function(async_func, retries=3):
    for attempt in range(retries):
        try:
            await async_func()
            return
        except KasaException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt + 1 == retries:
                print("All attempts failed.")
            else:
                await asyncio.sleep(2)  # Wait before retrying

# Wrapper to run the async functions from tkinter buttons
def run_async_function(async_func):
    asyncio.run(retry_async_function(async_func))

# Function to schedule the plug to turn on/off at a specific time
def schedule_plug_actions():
    global turn_on_time, turn_off_time
    while True:
        current_time = datetime.now().strftime("%H:%M")
        if turn_on_time == current_time:
            run_async_function(turn_on_plug)
        if turn_off_time == current_time:
            run_async_function(turn_off_plug)
        time.sleep(60)  # Check every minute

# Start the scheduling thread
def start_scheduler():
    scheduler_thread = threading.Thread(target=schedule_plug_actions)
    scheduler_thread.daemon = True
    scheduler_thread.start()

# Function to set the time for turning the plug on
def set_turn_on_time():
    global turn_on_time
    turn_on_time = on_time_entry.get()
    print(f"Scheduled turn on at {turn_on_time}")

# Function to set the time for turning the plug off
def set_turn_off_time():
    global turn_off_time
    turn_off_time = off_time_entry.get()
    print(f"Scheduled turn off at {turn_off_time}")

# Create the customtkinter application
ctk.set_appearance_mode("System")  # Can be "Light" or "Dark" mode
ctk.set_default_color_theme("blue")  # Can change to other themes like "dark-blue"

app = ctk.CTk()  # Create a CTk window
app.title("Smart Plug Controller")
app.geometry("900x600")  # Set window size

# Create a TabView
tabview = ctk.CTkTabview(master=app)
tabview.pack(padx=20, pady=20, fill="both", expand=True)

tabview.add("Manual Mode")  # Add tab for manual controls
tabview.add("Auto Mode")  # Add tab for auto controls
tabview.set("Manual Mode")  # Set initial visible tab

# Manual Mode Buttons and Frame (within the "Manual Mode" tab)
manual_mode_frame = ctk.CTkFrame(master=tabview.tab("Manual Mode"))
manual_mode_frame.pack(padx=20, pady=10, anchor="center", fill="x")  # Align at the center with some padding to move it up

# Add the buttons to the manual frame
on_button = ctk.CTkButton(master=manual_mode_frame, text="Turn On", command=lambda: run_async_function(turn_on_plug))
off_button = ctk.CTkButton(master=manual_mode_frame, text="Turn Off", command=lambda: run_async_function(turn_off_plug))
on_button.grid(row=0, column=0, padx=10, pady=10)
off_button.grid(row=0, column=1, padx=10, pady=10)

# Frame to organize widgets in a row (within the "Manual Mode" tab)
time_frame = ctk.CTkFrame(master=manual_mode_frame)
time_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

# Widgets to input the time for scheduling (left and right alignment)
on_time_label = ctk.CTkLabel(time_frame, text="Turn On Time (HH:MM):")
on_time_label.grid(row=0, column=0, padx=20, pady=5)

on_time_entry = ctk.CTkEntry(time_frame, placeholder_text="Enter time")
on_time_entry.grid(row=0, column=1, padx=20, pady=5)

set_on_time_button = ctk.CTkButton(time_frame, text="Set Turn On Time", command=set_turn_on_time)
set_on_time_button.grid(row=1, column=0, columnspan=2, pady=10)

off_time_label = ctk.CTkLabel(time_frame, text="Turn Off Time (HH:MM):")
off_time_label.grid(row=0, column=2, padx=20, pady=5)

off_time_entry = ctk.CTkEntry(time_frame, placeholder_text="Enter time")
off_time_entry.grid(row=0, column=3, padx=20, pady=5)

set_off_time_button = ctk.CTkButton(time_frame, text="Set Turn Off Time", command=set_turn_off_time)
set_off_time_button.grid(row=1, column=2, columnspan=2, pady=10)

import asyncio
import threading

# Global variable to control stopping PWM
pwm_running = False

# Function to control fan efficiency by simulating PWM
async def pwm_control(duty_cycle, duration=60):
    """
    Controls the fan by turning the plug on and off at intervals to simulate different efficiencies.
    duty_cycle: Percentage of time the plug should be on (0-100)
    duration: Total time to run the PWM in seconds (default is 60 seconds)
    """
    global pwm_running
    pwm_running = True  # Set flag to indicate PWM is running

    on_time = duty_cycle / 100 * 10  # Calculate on-time based on duty cycle (interval = 10 seconds)
    off_time = 10 - on_time  # Off-time is the rest of the 10-second interval

    plug = SmartPlug(PLUG_IP)
    await plug.update()

    end_time = time.time() + duration  # Run PWM control for the specified duration
    while time.time() < end_time and pwm_running:  # Only run if pwm_running is True
        try:
            await plug.turn_on()
            print(f"Plug turned on for {on_time} seconds.")
            await asyncio.sleep(on_time)
            
            await plug.turn_off()
            print(f"Plug turned off for {off_time} seconds.")
            await asyncio.sleep(off_time)
        except KasaException as e:
            print(f"Failed to control the plug: {e}")
            break  # Exit if there's an error

    print("PWM control stopped.")

# Function to start the PWM control in a background thread
def start_pwm_thread(duty_cycle):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(pwm_control(duty_cycle))

def start_pwm(duty_cycle):
    pwm_thread = threading.Thread(target=start_pwm_thread, args=(duty_cycle,))
    pwm_thread.daemon = True
    pwm_thread.start()
        

# Function to stop the PWM control
def stop_pwm():
    global pwm_running
    pwm_running = False
    print("PWM mode stopped by user.")


pwm_frame = ctk.CTkFrame(master=manual_mode_frame)
pwm_frame.grid(row=2, column=0, columnspan=3, pady=20, padx=10)
# Adding a dropdown menu to the GUI for user to select efficiency level
efficiency_label = ctk.CTkLabel(pwm_frame, text="Fan Efficiency (0-100%):")
efficiency_label.grid(row=0, column=0, padx=10, pady=10)

efficiency_slider = ctk.CTkSlider(pwm_frame, from_=0, to=100, number_of_steps=10)
efficiency_slider.grid(row=0, column=3, padx=10, pady=10)

pwm_button = ctk.CTkButton(master=pwm_frame, text="Start PWM Control", command=lambda: start_pwm(efficiency_slider.get()))
pwm_button.grid(row=1, column=0, padx=10, pady=10)

stop_pwm_button = ctk.CTkButton(master=pwm_frame, text="Stop PWM Control", command=stop_pwm)
stop_pwm_button.grid(row=1, column=3, padx=10, pady=10)
# Start the scheduling thread
start_scheduler()

# Global variables for storing the upper and lower temperature limits
upper_temp_limit = None
lower_temp_limit = None
current_temp = 25  # Simulated current temperature (replace with actual sensor reading in real application)

# Function to simulate reading the current temperature (replace this with actual sensor data)
def read_temperature():
    # For now, this is a simple placeholder to simulate temperature changes
    humidity, current_temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    
    return current_temp

# Function to automatically control the plug based on temperature
async def auto_control_plug():
    print("auto_control_plug")
    global upper_temp_limit, lower_temp_limit, pwm_running
    
    plug = SmartPlug(PLUG_IP)
    await plug.update()
    
    while True:
        temperature = read_temperature()  # Simulated temperature reading
        print(f"Current temperature: {temperature}")

        if upper_temp_limit and temperature >= upper_temp_limit and not plug.is_on:
            # Temperature exceeds upper limit, turn on plug
            await plug.turn_on()
            print("Plug turned on due to high temperature.")
            if pwm_running:
                # Start PWM if it is enabled
                await pwm_control(efficiency_slider.get())

        elif lower_temp_limit and temperature <= lower_temp_limit and plug.is_on:
            # Temperature drops below lower limit, turn off plug
            await plug.turn_off()
            print("Plug turned off due to low temperature.")
        
        # Wait some time before checking the temperature again
        await asyncio.sleep(5)  # Check temperature every 5 seconds

# Function to set the upper temperature limit
def set_upper_temp_limit():
    global upper_temp_limit
    upper_temp_limit = float(upper_temp_entry.get())
    print(f"Upper temperature limit set to {upper_temp_limit}")

# Function to set the lower temperature limit
def set_lower_temp_limit():
    global lower_temp_limit
    lower_temp_limit = float(lower_temp_entry.get())
    print(f"Lower temperature limit set to {lower_temp_limit}")

# Function to start the auto mode in a background thread
def start_auto_mode():
    auto_thread = threading.Thread(target=lambda: asyncio.run(auto_control_plug()))
    auto_thread.daemon = True
    auto_thread.start()

# Function to stop auto mode (by stopping the PWM)
def stop_auto_mode():
    global pwm_running
    pwm_running = False  # Stop any ongoing PWM
    print("Auto mode stopped by user.")

# Create the "Auto Mode" tab widgets
auto_mode_frame = ctk.CTkFrame(master=tabview.tab("Auto Mode"))
auto_mode_frame.pack(padx=20, pady=10, anchor="center", fill="x")

# Frame to organize widgets in a row (within the "Manual Mode" tab)
auto_mode_temp_frame = ctk.CTkFrame(master=auto_mode_frame)
auto_mode_temp_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

def update_temp_label():
    current_temp = read_temperature()
    current_temp_label.configure(text=f"Current Temperature: {current_temp:.2f} degrees")
    app.after(1000, update_temp_label)

current_temp_label = ctk.CTkLabel(auto_mode_temp_frame, text=f"Current Temperature: {current_temp}")
current_temp_label.grid(row=1, column=0, padx=10, pady=10)

update_temp_label()

# Input fields for upper and lower temperature limits
upper_temp_label = ctk.CTkLabel(auto_mode_temp_frame, text="Upper Temperature Limit (°C):")
upper_temp_label.grid(row=0, column=1, padx=10, pady=10)

upper_temp_entry = ctk.CTkEntry(auto_mode_temp_frame, placeholder_text="Enter upper limit")
upper_temp_entry.grid(row=0, column=2, padx=10, pady=10)

set_upper_temp_button = ctk.CTkButton(auto_mode_temp_frame, text="Set Upper Limit", command=set_upper_temp_limit)
set_upper_temp_button.grid(row=0, column=3, padx=10, pady=10)

lower_temp_label = ctk.CTkLabel(auto_mode_temp_frame, text="Lower Temperature Limit (°C):")
lower_temp_label.grid(row=3, column=1, padx=10, pady=10)

lower_temp_entry = ctk.CTkEntry(auto_mode_temp_frame, placeholder_text="Enter lower limit")
lower_temp_entry.grid(row=3, column=2, padx=10, pady=10)

set_lower_temp_button = ctk.CTkButton(auto_mode_temp_frame, text="Set Lower Limit", command=set_lower_temp_limit)
set_lower_temp_button.grid(row=3, column=3, padx=10, pady=10)

# Button to start auto mode
start_auto_button = ctk.CTkButton(auto_mode_temp_frame, text="Start Auto Mode", command=start_auto_mode)
start_auto_button.grid(row=4, column=1, padx=10, pady=10)

# Button to stop auto mode
stop_auto_button = ctk.CTkButton(auto_mode_temp_frame, text="Stop Auto Mode", command=stop_auto_mode)
stop_auto_button.grid(row=4, column=2, padx=10, pady=10)

pwm_frame_auto = ctk.CTkFrame(master=auto_mode_frame)
pwm_frame_auto.grid(row=5, column=0, columnspan=3, pady=20, padx=10)

efficiency_label_auto = ctk.CTkLabel(pwm_frame_auto, text="Fan Efficiency (0-100%):")
efficiency_label_auto.grid(row=0, column=1, padx=10, pady=10)

efficiency_slider_auto = ctk.CTkSlider(pwm_frame_auto, from_=0, to=100, number_of_steps=10)
efficiency_slider_auto.grid(row=0, column=3, padx=10, pady=10)

pwm_button_auto = ctk.CTkButton(master=pwm_frame_auto, text="Start PWM Control", command=lambda: start_pwm(efficiency_slider.get()))
pwm_button_auto.grid(row=1, column=1, padx=10, pady=10)

stop_pwm_button_auto = ctk.CTkButton(master=pwm_frame_auto, text="Stop PWM Control", command=stop_pwm)
stop_pwm_button_auto.grid(row=1, column=3, padx=10, pady=10)

# Function to collect the smart plug's stats
async def get_plug_stats():
    plug = SmartPlug(PLUG_IP)
    await plug.update()

    if plug.has_emeter:  # Check if the plug supports energy monitoring
        stats = {
            "Current Power (W)": plug.emeter_realtime["power"],
            "Total Energy (Wh)": plug.emeter_realtime["total"],
            "Voltage (V)": plug.emeter_realtime["voltage"],
            "Current (A)": plug.emeter_realtime["current"],
            "Consumption Today (kWh)" : plug.emeter_today,
            "Consumption This Month(kWh)" : plug.emeter_this_month,
            #"Total Runtime (minutes)": plug.uptime.total_seconds() / 60  # Convert seconds to minutes
        }
        return stats
    else:
        return {"Error": "This plug does not support energy monitoring"}

# Function to update the stats panel in the GUI
def update_stats_panel():
    stats = asyncio.run(get_plug_stats())  # Fetch plug stats
    if "Error" in stats:
        stats_label.config(text=stats["Error"])
    else:
        stats_text = "\n".join([f"{key}: {value}" for key, value in stats.items()])
        stats_label.configure(text=stats_text)

# Create a frame for displaying the plug stats
stats_frame = ctk.CTkFrame(master=app)
stats_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Add a label to display the stats
stats_label = ctk.CTkLabel(master=stats_frame, text="Smart Plug Stats will be displayed here.", justify="left")
stats_label.pack(padx=10, pady=10)

# Add a button to refresh stats manually
refresh_button = ctk.CTkButton(master=stats_frame, text="Refresh Stats", command=update_stats_panel)
refresh_button.pack(pady=10)

def start_auto_refresh_stats():
    while True:
        update_stats_panel()
        time.sleep(60)  # Refresh every 60 seconds

# Start the auto-refresh in a background thread (optional)
refresh_thread = threading.Thread(target=start_auto_refresh_stats)
refresh_thread.daemon = True
refresh_thread.start()


# Start the customtkinter event loop
app.mainloop()

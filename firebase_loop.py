import asyncio
from kasa import SmartPlug
import firebase_admin
from firebase_admin import credentials, db
from gpiozero import MotionSensor
from datetime import datetime
import time

# Replace with the IP address of your HS110
PLUG_IP = "192.168.2.30"

# Path to your Firebase Admin SDK credentials file
cred_path = "creds.json"

# Initialize Firebase connection
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smart-energy-d9721-default-rtdb.firebaseio.com/'  # Replace with your Firebase Realtime Database URL
})

# Firebase reference
ref = db.reference('smart_home/plug_states')

# Initialize the motion sensor (GPIO 17 assumed for PIR sensor)
pir = MotionSensor(17)

# Initialize plug state tracking
plug_on = False
no_motion_since = None  # Keeps track of when no motion was first detected
in_delay = False  # Tracks whether we are in the 5-second delay

# Function to log state changes to Firebase
def log_to_firebase(state, power):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ref.push({
        'timestamp': timestamp,
        'status': state,
        'power_consumption': power
    })
    print(f"Logged to Firebase: {state} at {timestamp}")

async def monitor_plug():
    global plug_on, no_motion_since, in_delay
    plug = SmartPlug(PLUG_IP)

    while True:
        # Update plug state information
        await plug.update()
        
        if plug_on:
            log_to_firebase('on', plug.emeter_realtime['power'])
        if not plug_on:
            log_to_firebase('off', plug.emeter_realtime['power'])
        # Case 1: Motion detected
        if pir.motion_detected:
            print("Motion detected!")
            no_motion_since = None  # Reset no-motion timer
            in_delay = False  # Cancel any pending turn-off delay
            
            if not plug_on:
                print("Turning the plug ON")
                await plug.turn_on()
                plug_on = True

                # Log the state change to Firebase
                #await plug.update()
                #log_to_firebase('on', plug.emeter_realtime['power'])

        # Case 2: No motion detected
        else:
            # Set no_motion_since only the first time motion is lost
            if no_motion_since is None:
                no_motion_since = time.time()  # Record the time when motion first stops
                print(f"No motion detected, starting timer at {no_motion_since}")

            # Check if 10 seconds have passed since no motion was detected
            elif time.time() - no_motion_since >= 10 and plug_on and not in_delay:
                print("No motion detected for 10 seconds, waiting 5 more seconds...")
                in_delay = True  # Start the 5-second delay
                delay_start = time.time()  # Track when the delay starts

                # Continue checking for 5 seconds before turning the plug OFF
                while time.time() - delay_start < 5:
                    if pir.motion_detected:
                        print("Motion detected during delay, keeping the plug ON")
                        no_motion_since = None  # Reset the timer if motion is detected
                        in_delay = False  # Cancel the delay
                        break
                    await asyncio.sleep(1)  # Check every second within the 5-second delay

                # If delay finishes without motion, turn the plug OFF
                if in_delay:  # Ensure we're still in the delay period and no motion was detected
                    print("Turning the plug OFF after 15 seconds of no motion")
                    await plug.turn_off()
                    plug_on = False
                    in_delay = False  # Reset the delay flag

                    # Log the state change to Firebase
                    await plug.update()
                    log_to_firebase('off', plug.emeter_realtime['power'])

        # Wait for 5 seconds before checking again
        await asyncio.sleep(5)

# Run the asyncio loop
if __name__ == "__main__":
    try:
        asyncio.run(monitor_plug())
    except KeyboardInterrupt:
        print("Monitoring stopped.")





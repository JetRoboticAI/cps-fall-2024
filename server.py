from flask import Flask, request, jsonify
import time
import os

# Initialize Flask app
app = Flask(__name__)

# Set path to the desktop file
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "data.txt")

# Route for handling POST requests at the root URL
@app.route('/', methods=['GET', 'POST'])
def receive_activation_time():
    # Check the HTTP method
    print(f"Request method: {request.method}")  # Log the request method for debugging
    
    if request.method == 'POST':
        # Retrieve JSON data from the request
        data = request.get_json()
        
        # Check if activation_time is in the data
        if data and "activation_time" in data:
            activation_time = data["activation_time"]

            # Convert activation time from milliseconds to a readable format
            try:
                formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(activation_time) / 1000))
                print(f"Servo activated at: {formatted_time}")

                # Log data to the local file on the desktop
                with open(desktop_path, 'a') as file:
                    file.write(f"Servo activated at: {formatted_time}\n")

            except ValueError:
                return jsonify({"status": "error", "message": "Invalid activation_time format"}), 400

            # Send a JSON response indicating success
            return jsonify({"status": "success", "received_time": formatted_time}), 200
        else:
            # If activation_time is not in data, respond with an error
            return jsonify({"status": "error", "message": "Invalid data, 'activation_time' missing"}), 400
    else:
        # Response for GET requests (useful for testing if the server is running)
        return "This endpoint is ready to receive POST requests.", 200

# Run the app on all available network interfaces and on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

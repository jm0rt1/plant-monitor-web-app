from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Replace with your Arduino's IP address
arduino_ip = '192.168.1.X'  # Adjust the IP address
arduino_port = 80  # Port number (default is 80)


@app.route('/')
def index():
    return 'Welcome to the Flask Server!'


@app.route('/get_sensor_data')
def get_sensor_data():
    try:
        # Construct the URL to request sensor data
        url = f'http://192.168.4.58:{80}'

        # Send GET request to the Arduino
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Get sensor value from Arduino's response
        sensor_value = response.text.strip()

        # Return the sensor value as JSON
        return sensor_value

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Run the Flask server on all available interfaces (0.0.0.0)
    app.run(host='0.0.0.0', port=7070)

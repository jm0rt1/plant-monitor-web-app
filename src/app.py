from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import base64
import io
import matplotlib.pyplot as plt
from flask import Flask, jsonify, render_template
import requests
import matplotlib
# Use a non-interactive backend suitable for server environments
matplotlib.use('Agg')

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Replace with your Arduino's IP address
arduino_ip = '192.168.1.X'  # Adjust the IP address
arduino_port = 80  # Port number

# Define the database model


class SensorReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(
        db.DateTime, default=datetime.now())
    sensor_value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<SensorReading {self.id} - {self.sensor_value}>'


# Create the database tables
with app.app_context():
    db.create_all()


@ app.route('/')
def index():
    return 'Welcome to the Flask Server!'


@ app.route('/get_sensor_data')
def get_sensor_data():
    try:
        # Construct the URL to request sensor data
        url = f'http://192.168.4.58:80'

        # Send GET request to the Arduino
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Get sensor value from Arduino's response
        sensor_value = float(response.text.split(":")[-1].strip())

        # Store the sensor value in the database
        new_reading = SensorReading(sensor_value=sensor_value)
        db.session.add(new_reading)
        db.session.commit()

        # Return the sensor value as JSON
        return jsonify({'sensor_value': sensor_value})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


@ app.route('/plot')
def plot():
    # Fetch data from the database
    readings = SensorReading.query.order_by(SensorReading.timestamp).all()

    # Extract timestamps and sensor values
    timestamps = [reading.timestamp for reading in readings]
    sensor_values = [reading.sensor_value for reading in readings]

    # Create the plot
    fig, ax = plt.subplots()
    ax.plot(timestamps, sensor_values, marker='o')
    ax.set_title('Sensor Data Over Time')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Sensor Value')
    ax.grid(True)
    fig.autofmt_xdate()

    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    # Encode the plot image to display in HTML
    image_base64 = base64.b64encode(buf.getvalue()).decode('ascii')

    # Render the HTML template with the plot
    return render_template('plot.html', image_base64=image_base64)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7070)

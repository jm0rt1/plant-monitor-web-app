from flask import Flask, jsonify, render_template
import requests
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import DatetimeTickFormatter
from bokeh.resources import CDN


app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Replace with your Arduino's IP address
arduino_ip = '192.168.4.58'  # Adjust the IP address
arduino_port = 80  # Port number

# Define the database model


class SensorReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sensor_value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<SensorReading {self.id} - {self.sensor_value}>'


# Create the database tables
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return 'Welcome to the Flask Server!'


@app.route('/get_sensor_data')
def get_sensor_data():
    try:
        # Construct the URL to request sensor data
        url = f'http://{arduino_ip}:{arduino_port}/'

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


@app.route('/plot')
def plot():
    # Fetch data from the database
    readings = SensorReading.query.order_by(SensorReading.timestamp).all()
    timestamps = [reading.timestamp for reading in readings]
    sensor_values = [reading.sensor_value for reading in readings]

    # Create a Bokeh plot with updated parameters
    plot = figure(
        title='Sensor Data Over Time',
        x_axis_type='datetime',
        width=800,
        height=400
    )

    # Plot the line
    plot.line(
        x=timestamps,
        y=sensor_values,
        line_width=2,
        legend_label='Sensor Value',
    )

    # Plot the scatter points using 'scatter' instead of 'circle'
    plot.scatter(
        x=timestamps,
        y=sensor_values,
        fill_color="white",
        size=8,
    )

    # Configure axes
    plot.xaxis.axis_label = 'Timestamp'
    plot.yaxis.axis_label = 'Sensor Value'
    plot.xaxis.formatter = DatetimeTickFormatter(
        hours="%H:%M",
        days="%d %b",
        months="%d %b %Y",
        years="%d %b %Y",
    )
    plot.xaxis.major_label_orientation = 0.5

    # Generate the script and div components
    script, div = components(plot)
    # Get the Bokeh CSS and JS resources
    bokeh_css = CDN.render_css()
    bokeh_js = CDN.render_js()
    # Render the template
    return render_template('bokeh_plot.html', script=script, div=div, bokeh_css=bokeh_css, bokeh_js=bokeh_js)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7070)

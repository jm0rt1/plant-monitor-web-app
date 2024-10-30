from bokeh.models import AjaxDataSource, CustomJS
from flask import Flask, jsonify, redirect, render_template, request, url_for
import requests
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler as sch

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import DatetimeTickFormatter
from bokeh.resources import CDN, INLINE
from bokeh.models import AjaxDataSource


app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Replace with your Arduino's IP address
arduino_ip = '192.168.4.58'  # Adjust the IP address
arduino_port = 80  # Port number


scheduler = sch()
scheduler.start()


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


@app.route('/data')
def data():
    # Fetch data from the database
    readings = SensorReading.query.order_by(SensorReading.timestamp).all()
    # Prepare data for AjaxDataSource
    data = {
        'x': [reading.timestamp.isoformat() for reading in readings],
        'y': [reading.sensor_value for reading in readings],
    }
    return jsonify(data)


@app.route('/plot')
def plot():
    source = AjaxDataSource(
        data_url=url_for('data', _external=True),
        polling_interval=2000,
        method='GET',
        mode='replace',
        content_type='application/json'
    )
    # source.callback = CustomJS(code="""
    #     const result = cb_data.response;
    #     source.data = {
    #         x: result.x.map(ts => ts),  // Timestamps are already in milliseconds
    #         y: result.y
    #     };
    #     source.change.emit();
    # """, args={'source': source})

    plot = figure(
        title='Sensor Data Over Time',
        x_axis_type='datetime',
        width=800,
        height=400,
        tools='pan,wheel_zoom,box_select,lasso_select,tap,reset'
    )

    plot.line(
        x='x',
        y='y',
        source=source,
        line_width=2,
        legend_label='Sensor Value',
    )

    plot.circle(
        x='x',
        y='y',
        source=source,
        size=8,
        fill_color='white',
        selection_color='firebrick',
        nonselection_fill_color='gray',
        nonselection_fill_alpha=0.2
    )

    plot.xaxis.axis_label = 'Timestamp'
    plot.yaxis.axis_label = 'Sensor Value'
    plot.xaxis.formatter = DatetimeTickFormatter(
        milliseconds="%H:%M:%S",
        seconds="%H:%M:%S",
        minsec="%H:%M:%S",
        minutes="%H:%M",
        hourmin="%H:%M",
        hours="%H:%M",
        days="%d %b",
        months="%b %Y",
        years="%Y",
    )
    plot.xaxis.major_label_orientation = 0.5

    script, div = components(plot)
    bokeh_css = INLINE.render_css()
    bokeh_js = INLINE.render_js()
    return render_template('bokeh_plot.html', script=script, div=div, bokeh_css=bokeh_css, bokeh_js=bokeh_js)


@app.route('/set_interval', methods=['GET', 'POST'])
def set_interval():

    if request.method == 'POST':
        new_interval = int(request.form['interval'])
        # Update the job interval
        scheduler.reschedule_job(
            'poll_sensor_job', trigger='interval', seconds=new_interval)
        return redirect(url_for('set_interval'))
    else:
        # Get current interval
        job = scheduler.get_job('poll_sensor_job')
        interval = job.trigger.interval.total_seconds()
        return render_template('set_interval.html', interval=interval)


def poll_sensor_data():
    with app.app_context():
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

        except requests.exceptions.RequestException as e:
            print(f"Error polling sensor data: {e}")


scheduler.add_job(
    id='poll_sensor_job',
    func=poll_sensor_data,
    trigger='interval',
    seconds=1  # Default interval
)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7070)

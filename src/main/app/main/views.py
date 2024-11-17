from typing import List, Dict, Any
from flask import render_template
import json
import plotly
import plotly.graph_objects as go
from flask import Blueprint, render_template, redirect, url_for, flash
from ..database.implementations.database_manager import DatabaseManager
from ..devices.factories.sensor_device_factory import SensorDeviceFactory
from ..visualization.implementations.visualizer import Visualizer
from ..utils.logger import get_logger

db_manager = DatabaseManager()
device_factory = SensorDeviceFactory()
visualizer = Visualizer()
logger = get_logger(__name__)

# Other imports...

# Define the Blueprint here
main = Blueprint('main', __name__)

# Rest of the code...

db_manager = DatabaseManager()


def generate_temperature_plot(sensor_data: List[Dict[str, Any]]) -> str:
    timestamps = [data['timestamp'] for data in sensor_data]
    temperatures = [data['data']['temperature'] for data in sensor_data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=temperatures,
                  mode='lines+markers', name='Temperature'))
    fig.update_layout(
        title='Temperature Plot',
        xaxis_title='Timestamp',
        yaxis_title='Temperature'
    )
    return fig.to_html(full_html=False)


def generate_humidity_plot(sensor_data: List[Dict[str, Any]]) -> str:
    timestamps = [data['timestamp'] for data in sensor_data]
    humidities = [data['data']['humidity'] for data in sensor_data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=humidities,
                  mode='lines+markers', name='Humidity'))
    fig.update_layout(
        title='Humidity Plot',
        xaxis_title='Timestamp',
        yaxis_title='Humidity'
    )
    return fig.to_html(full_html=False)


def generate_soil_moisture_plot(sensor_data: List[Dict[str, Any]]) -> str:
    timestamps = [data['timestamp'] for data in sensor_data]
    soil_moisture = [data['soil_moisture'] for data in sensor_data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=soil_moisture,
                  mode='lines+markers', name='Soil Moisture'))
    fig.update_layout(
        title='Soil Moisture Plot',
        xaxis_title='Timestamp',
        yaxis_title='Soil Moisture'
    )
    return fig.to_html(full_html=False)


@main.route('/')
def index():

    devices = db_manager.get_all_devices()

    return render_template('index.html', devices=devices)


@main.route('/device/<device_id>')
def device_detail(device_id):
    device_info = db_manager.get_device_info(device_id)
    sensor_data = db_manager.get_sensor_data(device_id)

    timestamps = [data['timestamp'] for data in sensor_data]
    temperatures = [data['data']['temperature'] for data in sensor_data]
    # Create the plot
    temperature_trace = go.Scatter(
        x=timestamps,
        y=temperatures,
        mode='lines+markers',
        name='Temperature'
    )

    layout = go.Layout(
        title='Temperature Plot',
        xaxis=dict(title='Timestamp'),
        yaxis=dict(title='Temperature')
    )

    fig = go.Figure(data=[temperature_trace], layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('device_detail.html', graphJSON=graphJSON)


@main.route('/collect-data')
def collect_data():
    device_ips = ['192.168.1.10', '192.168.1.11']  # Replace with actual IPs
    for ip in device_ips:
        device = device_factory.create_sensor_device(ip_address=ip)
        try:
            data = device.get_sensor_data()
            db_manager.save_sensor_data(data)
            info = device.get_device_info()
            db_manager.save_device_info(info)
        except Exception as e:
            logger.error(f"Error collecting data from device {ip}: {e}")
    flash('Data collection completed.')
    return redirect(url_for('.index'))

# Route that displays a table with all the data


@main.route('/data-table')
def data_table():
    sensor_data = db_manager.get_sensor_data(1)
    return render_template('data_table.html', sensor_data=sensor_data)

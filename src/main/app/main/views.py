from flask import render_template, redirect, url_for, flash
from . import main
from ..database.implementations.database_manager import DatabaseManager
from ..devices.factories.sensor_device_factory import SensorDeviceFactory
from ..visualization.implementations.visualizer import Visualizer
from ..utils.logger import get_logger

db_manager = DatabaseManager()
device_factory = SensorDeviceFactory()
visualizer = Visualizer()
logger = get_logger(__name__)


@main.route('/')
def index():
    devices = db_manager.get_all_devices()
    return render_template('index.html', devices=devices)


@main.route('/device/<device_id>')
def device_detail(device_id):
    device_info = db_manager.get_device_info(device_id)
    sensor_data = db_manager.get_sensor_data(device_id)
    graph = visualizer.generate_plot(sensor_data)
    return render_template('device_detail.html', device_info=device_info, graph=graph)


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

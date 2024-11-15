
import random
import sys  # noqa
import os  # noqa

# Get the directory of the current script (scripts directory)
current_dir = os.path.dirname(os.path.abspath(__file__))  # noqa

# Add the scripts directory to sys.path
if current_dir not in sys.path:  # noqa
    sys.path.insert(0, current_dir)  # noqa

# Now you can import setup_paths
import setup_paths  # noqa

# ... rest of your imports
import datetime  # noqa
from src.main.app import create_app, db  # noqa
from src.main.app.database.models import DeviceInfo, SensorData  # noqa


def create_development_database():
    app = create_app(config_name='development')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        # Initialize the database
        # db.init_app(app)
        db.create_all()

        # Insert sample DeviceInfo data
        device1 = DeviceInfo(

            device_name='Test Device 1',
            firmware_version='1.0.0',
            last_seen=datetime.datetime.utcnow(),
            additional_info={'location': 'Office'}
        )
        device2 = DeviceInfo(

            device_name='Test Device 2',
            firmware_version='1.1.0',
            last_seen=datetime.datetime.utcnow(),
            additional_info={'location': 'Lab'}
        )
        db.session.add_all([device1, device2])
        db.session.commit()
        now = datetime.datetime.utcnow()
        data = []
        for i in range(0, 400):

            time_delta = datetime.timedelta(seconds=i)
            stamp = now - time_delta
            sensor_data = SensorData(
                device_id=1,
                timestamp=stamp,
                data={'temperature': 22.5 +
                      random.randint(-10, 10), 'humidity': 45 +
                      random.randint(-10, 10)}
            )
            data.append(sensor_data)
        data.reverse()
        # Insert sample SensorData linked to devices
        db.session.add_all(data)
        db.session.commit()


if __name__ == '__main__':
    create_development_database()

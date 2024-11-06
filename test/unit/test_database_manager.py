import unittest
from src.main.app.database.implementations.database_manager import DatabaseManager, db
from src.main.app import create_app, ConfigType
import os


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        os.environ['FLASK_CONFIG'] = 'test'
        app = create_app(ConfigType.test)
        app.app_context().push()
        db.create_all()
        self.db_manager = DatabaseManager()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_save_and_get_device_info(self):
        device_info = {
            'device_name': 'device123',
            'firmware_version': '1.0.0',
            'additional_info': {}
        }
        self.db_manager.save_device_info(device_info)
        retrieved_info = self.db_manager.get_device_info('device123')
        self.assertEqual(retrieved_info['firmware_version'], '1.0.0')

    def test_save_and_get_sensor_data(self):
        sensor_data = {
            'device_id': 1,
            'timestamp': '2023-01-01T12:00:00',
            'data': {'temperature': 25, 'humidity': 50}
        }
        self.db_manager.save_sensor_data(sensor_data)
        retrieved_data = self.db_manager.get_sensor_data(1)
        self.assertEqual(len(retrieved_data), 1)
        self.assertEqual(retrieved_data[0]['data']['temperature'], 25)

    def test_build_test_database(self):
        build_test_database(self.db_manager)
        retrieved_info = self.db_manager.get_device_info('device123')
        self.assertEqual(retrieved_info['firmware_version'], '1.0.0')
        retrieved_data = self.db_manager.get_sensor_data(1)
        self.assertEqual(len(retrieved_data), 60)


def build_test_database(db_manager: DatabaseManager):
    device_info = {
        'device_name': 'device123',
        'firmware_version': '1.0.0',
        'additional_info': {}
    }
    db_manager.save_device_info(device_info)

    # Generate a lot of mock sensor data for device123
    for i in range(60):

        sensor_data = {
            'device_id': 1,
            'timestamp': f'2023-01-01T12:{i:02d}:00',
            'data': {'temperature': 25 + i, 'humidity': 50 - i}
        }
        db_manager.save_sensor_data(sensor_data)


if __name__ == '__main__':
    unittest.main()

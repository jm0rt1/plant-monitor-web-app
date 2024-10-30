import unittest
from src.main.app.database.implementations.database_manager import DatabaseManager
from src.main.app import create_app, db
from src.main.app.main.models import DeviceInfo, SensorData
import os


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        os.environ['FLASK_CONFIG'] = 'testing'
        app = create_app('testing')
        app.app_context().push()
        db.create_all()
        self.db_manager = DatabaseManager()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_save_and_get_device_info(self):
        device_info = {
            'device_id': 'device123',
            'firmware_version': '1.0.0',
            'additional_info': {}
        }
        self.db_manager.save_device_info(device_info)
        retrieved_info = self.db_manager.get_device_info('device123')
        self.assertEqual(retrieved_info['firmware_version'], '1.0.0')


if __name__ == '__main__':
    unittest.main()

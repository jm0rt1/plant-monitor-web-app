import unittest
from src.main.run import app
from src.main.app import db
from src.main.app.main.models import DeviceInfo
import os


class TestApp(unittest.TestCase):
    def setUp(self):
        os.environ['FLASK_CONFIG'] = 'testing'
        self.app = app
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            device = DeviceInfo(device_id='device123',
                                firmware_version='1.0.0')
            db.session.add(device)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'device123', response.data)


if __name__ == '__main__':
    unittest.main()

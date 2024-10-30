import unittest
from src.main.app.devices.implementations.sensor_device import SensorDevice
from unittest.mock import patch


class TestSensorDevice(unittest.TestCase):
    def setUp(self):
        self.device = SensorDevice(ip_address='192.168.1.10')

    @patch('src.main.app.devices.implementations.sensor_device.requests.get')
    def test_get_sensor_data(self, mock_get):
        mock_get.return_value.json.return_value = {
            'device_id': 'device123',
            'timestamp': '2023-01-01T12:00:00',
            'data': {'temperature': 25}
        }
        mock_get.return_value.raise_for_status = lambda: None
        data = self.device.get_sensor_data()
        self.assertEqual(data['device_id'], 'device123')
        self.assertIn('temperature', data['data'])


if __name__ == '__main__':
    unittest.main()

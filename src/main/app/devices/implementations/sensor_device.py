from ...devices.interfaces.isensor_device import ISensorDevice
from typing import Dict, Any
import requests


class SensorDevice(ISensorDevice):
    def __init__(self, ip_address: str):
        self.ip_address = ip_address

    def get_sensor_data(self) -> Dict[str, Any]:
        try:
            response = requests.get(f'http://{self.ip_address}/sensor-data')
            response.raise_for_status()
            data = response.json()
            return {
                'device_id': data['device_id'],
                'timestamp': data['timestamp'],
                'data': data['data']
            }
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to get sensor data: {e}")

    def get_device_info(self) -> Dict[str, Any]:
        try:
            response = requests.get(f'http://{self.ip_address}/device-info')
            response.raise_for_status()
            info = response.json()
            return {
                'device_id': info['device_id'],
                'firmware_version': info['firmware_version'],
                'additional_info': info.get('additional_info', {})
            }
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to get device info: {e}")

    def update_firmware(self, firmware_data: bytes) -> bool:
        try:
            response = requests.post(
                f'http://{self.ip_address}/update-firmware',
                files={'firmware': firmware_data}
            )
            response.raise_for_status()
            return response.json().get('success', False)
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to update firmware: {e}")

from ..implementations.sensor_device import SensorDevice
from ..interfaces.isensor_device import ISensorDevice


class SensorDeviceFactory:
    def create_sensor_device(self, ip_address: str) -> ISensorDevice:
        return SensorDevice(ip_address=ip_address)

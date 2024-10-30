from abc import ABC, abstractmethod
from typing import Dict, Any


class ISensorDevice(ABC):
    @abstractmethod
    def get_sensor_data(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_device_info(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update_firmware(self, firmware_data: bytes) -> bool:
        pass

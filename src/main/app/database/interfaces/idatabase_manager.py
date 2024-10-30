from abc import ABC, abstractmethod
from typing import Dict, Any, List


class IDatabaseManager(ABC):
    @abstractmethod
    def save_sensor_data(self, data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def get_sensor_data(self, device_id: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def save_device_info(self, info: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def get_device_info(self, device_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_all_devices(self) -> List[Dict[str, Any]]:
        pass

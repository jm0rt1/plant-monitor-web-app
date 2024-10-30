from abc import ABC, abstractmethod
from ..devices.interfaces.isensor_device import ISensorDevice


class IFirmwareUpdater(ABC):
    @abstractmethod
    def check_for_updates(self) -> bool:
        pass

    @abstractmethod
    def get_firmware_data(self) -> bytes:
        pass

    @abstractmethod
    def push_update(self, device: ISensorDevice) -> bool:
        pass

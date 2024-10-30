from abc import ABC, abstractmethod
from typing import List, Dict


class IVisualizer(ABC):
    @abstractmethod
    def generate_plot(self, sensor_data: List[Dict[str, Any]]) -> str:
        pass

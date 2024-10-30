from ...database.interfaces.idatabase_manager import IDatabaseManager
from ...main.models import DeviceInfo, SensorData
from ... import db
from typing import Dict, Any, List
from datetime import datetime


class DatabaseManager(IDatabaseManager):
    def save_sensor_data(self, data: Dict[str, Any]) -> None:
        sensor_data = SensorData(
            device_id=data['device_id'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            data=data['data']
        )
        db.session.add(sensor_data)
        db.session.commit()

    def get_sensor_data(self, device_id: str) -> List[Dict[str, Any]]:
        records = SensorData.query.filter_by(device_id=device_id).all()
        return [record.to_dict() for record in records]

    def save_device_info(self, info: Dict[str, Any]) -> None:
        device_info = DeviceInfo.query.filter_by(
            device_id=info['device_id']).first()
        if not device_info:
            device_info = DeviceInfo(device_id=info['device_id'])
        device_info.firmware_version = info['firmware_version']
        device_info.last_seen = datetime.utcnow()
        device_info.additional_info = info.get('additional_info', {})
        db.session.add(device_info)
        db.session.commit()

    def get_device_info(self, device_id: str) -> Dict[str, Any]:
        device_info = DeviceInfo.query.filter_by(device_id=device_id).first()
        return device_info.to_dict() if device_info else {}

    def get_all_devices(self) -> List[Dict[str, Any]]:
        devices = DeviceInfo.query.all()
        return [device.to_dict() for device in devices]

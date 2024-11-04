from .. import db


class DeviceInfo(db.Model):
    __tablename__ = 'device_info'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(64), unique=True)
    firmware_version = db.Column(db.String(64))
    last_seen = db.Column(db.DateTime)
    additional_info = db.Column(db.JSON)

    def to_dict(self):
        return {
            'device_id': self.device_id,
            'firmware_version': self.firmware_version,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'additional_info': self.additional_info,
        }


class SensorData(db.Model):
    __tablename__ = 'sensor_data'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(
        db.String(64), db.ForeignKey('device_info.device_id'))
    timestamp = db.Column(db.DateTime)
    data = db.Column(db.JSON)

    def to_dict(self):
        return {
            'device_id': self.device_id,
            'timestamp': self.timestamp.isoformat(),
            'data': self.data,
        }

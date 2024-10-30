# API Documentation

## Endpoints

### GET /

- **Description**: Displays the list of devices.
- **Response**: Renders `index.html` with a list of devices.

### GET /device/<device_id>

- **Description**: Displays details and sensor data for a specific device.
- **Response**: Renders `device_detail.html` with device information and graph.

### GET /collect-data

- **Description**: Triggers data collection from all devices.
- **Response**: Redirects to the home page with a flash message.

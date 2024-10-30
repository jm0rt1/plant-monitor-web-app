├── app/
│   ├── __init__.py
│   ├── main/
│   │   ├── __init__.py
│   │   ├── controllers.py
│   │   ├── models.py
│   │   ├── views.py
│   │   └── templates/
│   │       └── ...
│   ├── devices/
│   │   ├── __init__.py
│   │   ├── interfaces/
│   │   │   └── isensor_device.py
│   │   ├── implementations/
│   │   │   └── sensor_device.py
│   │   └── factories/
│   │       └── sensor_device_factory.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── interfaces/
│   │   │   └── idatabase_manager.py
│   │   └── implementations/
│   │       └── database_manager.py
│   ├── firmware/
│   │   ├── __init__.py
│   │   ├── interfaces/
│   │   │   └── ifirmware_updater.py
│   │   └── implementations/
│   │       └── firmware_updater.py
│   ├── visualization/
│   │   ├── __init__.py
│   │   ├── interfaces/
│   │   │   └── ivisualizer.py
│   │   └── implementations/
│   │       └── visualizer.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logger.py
│   └── static/
│       └── ...
├── migrations/
│   └── ...
├── tests/
│   └── ...
├── config.py
├── requirements.txt
├── run.py
└── README.md

# setup.py

from setuptools import setup, find_packages

setup(
    name='my_sensor_app',
    version='1.0.0',
    packages=find_packages(where='src/main'),
    package_dir={'': 'src/main'},
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask_SQLAlchemy',
        'Flask_Migrate',
        'Flask_Bootstrap',
        'SQLAlchemy',
        'plotly',
        'pandas',
        # Other dependencies...
    ],
    entry_points={
        'console_scripts': [
            'runserver = app.run:main',
        ],
    },
)

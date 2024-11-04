import os

from app import create_app
import argparse
import app.utils.config as config


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str,
                        default='development', required=True, help="Config type. Use one of: development, production or default")
    args = parser.parse_args()
    if args.config not in config.config:
        raise ValueError(
            'Invalid config type. Use one of: development, production, test, or default')
    return args.config


if __name__ == '__main__':
    """take in the config type as an argument"""
    config_arg = parse_arguments()
    app = create_app(config_arg)

    app.run(port=5001)

#! /usr/bin/env python

from google_maps_travel_time_monitor import driver as app_driver
from google_maps_travel_time_monitor.app_runner import AppArgs
from google_maps_travel_time_monitor import app_runner
from pathlib import Path
from typing import Union
import click


@click.command()
@click.option('-c', '--config', required=True)
def main(config: Union[str, Path]):
    driver = app_driver.from_config(config)
    service_name = 'GOOGLE_MAPS_TRAVEL_TIME_MONITOR'
    app_args = AppArgs(service_name=service_name)
    app_runner.run(
        driver=driver,
        app_args=app_args
    )


if __name__ == "__main__":
    main()

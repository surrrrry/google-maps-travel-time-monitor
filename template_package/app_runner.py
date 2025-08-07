#! /usr/bin/env python

from template_package.driver import TemplateDriver
from template_package import core
from peaklib import driverutils
import schedule


class AppArgs:
    def __init__(self, service_name: str):
        self.service_name = service_name

    # TODO: ADD MORE ARGUMENTS AS NEEDED


def run(app_args: AppArgs, driver: TemplateDriver, auto_start: bool = True) -> None:
    driver.service_name = app_args.service_name

    # setup destination database stuff

    if driver.developer_mode_enabled:
        driver.destination_table = None

    # run setup routine
    driver.run_setup()

    # schedule task

    if auto_start:
        driverutils.run_schedule_forever()


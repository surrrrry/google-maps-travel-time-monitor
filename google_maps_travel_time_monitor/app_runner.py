#! /usr/bin/env python

from google_maps_travel_time_monitor.driver import GoogleMapsTravelTimeMonitor
from google_maps_travel_time_monitor import table_models
from google_maps_travel_time_monitor import core
from peaklib import driverutils
import schedule


class AppArgs:
    def __init__(self, service_name: str):
        self.service_name = service_name

    # TODO: ADD MORE ARGUMENTS AS NEEDED


def run(app_args: AppArgs, driver: GoogleMapsTravelTimeMonitor, auto_start: bool = True) -> None:
    driver.service_name = app_args.service_name

    # setup destination database stuff
    driver.destination_database_name = 'google_maps'
    if driver.developer_mode_enabled:
        driver.destination_table = table_models.get_snapshot_model('_travel_times_snapshot')
    else:
        driver.destination_table = table_models.get_snapshot_model('travel_times_snapshot')

    # run setup routine
    driver.run_setup()

    # schedule task
    driverutils.schedule_repeating_job(
        task_label='RUN SCHEDULED SERVICE',
        function=driver.run_basic_service_function,
        function_args=[
            core.run,
        ],
        interval_unit=driver.live_loop_interval_unit,
        interval_value=driver.live_loop_interval_value,
        driver=driver,
    )

    if driver.on_start_enabled:
        driverutils.run_thread(
            target=driver.run_basic_service_function,
            args=[
                core.run,
            ],
            thread_name='RUN ON-START SERVICE',
            driver=driver,
        )

    if auto_start:
        driverutils.run_schedule_forever()

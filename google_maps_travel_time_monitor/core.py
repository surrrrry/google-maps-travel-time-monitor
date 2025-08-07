#! /usr/bin/env python

from google_maps_travel_time_monitor.driver import GoogleMapsTravelTimeMonitor
from peaklib import driverutils
from peaklib import mysqlutils
from peaklib import timeutils
from peaklib import logger
from typing import List
import pandas as pd
import googlemaps
import re


@logger.service_function()
def run(driver: GoogleMapsTravelTimeMonitor, ) -> None:

    gmaps = googlemaps.Client(key=driver.get_google_maps_api_key())
    routes = [
        ["My Apartment to Tesla GFNV", "815 Kiley Pkwy, Sparks, NV 89436", "Tesla Gigafactory Nevada, Electric Ave, Sparks, NV 89434"],
        ["Tesla GFNV to my Apartment", "Tesla Gigafactory Nevada, Electric Ave, Sparks, NV 89434", '815 Kiley Pkwy, Sparks, NV 89436'],
    ]

    data = []
    for route_name, start, end in routes:
        result = gmaps.distance_matrix(
            start,
            end,
            mode="driving",
            departure_time="now",
            # traffic_model='pessimistic'
        )
        t = result['rows'][0]['elements'][0]['duration_in_traffic']['text']
        meters = result['rows'][0]['elements'][0]['distance']['value']
        miles = meters / 1609.34

        minutes = __parse_time_to_minutes(t)
        data.append({
            'utc_datetime': timeutils.get_current_datetime_utc(),
            'route_name': route_name,
            'start': start,
            'end': end,
            'miles': miles,
            'minutes': minutes,
        })
        print(data)

    df = pd.DataFrame(data)
    df['created_at'] = timeutils.get_current_datetime_utc()
    df['last_updated'] = timeutils.get_current_datetime_utc()

    __upsert(df, driver)
    __reset_auto_incrment(driver)


def __upsert(df: pd.DataFrame, driver: GoogleMapsTravelTimeMonitor) -> None:
    if df.empty:
        logger.log_upload_skipped_event(driver=driver)
        return

    stmt = mysqlutils.create_mysql_insert_stmt(
        table_model=driver.destination_table,
        df=df,
        append_ignore=True,
    )

    # stmt = stmt.on_duplicate_key_update(
        # todo
        # ...
        # key=stmt.inserted.key,
        # last_updated=stmt.inserted.last_updated,
    # )

    driverutils.upload(
        driver=driver,
        df=df,
        stmt=stmt,
        destination_database_name=driver.destination_database_name,
        destination_table_name=driver.destination_table.__tablename__,
        chunked_upsert=False,
        upsert_chunk_size=100000,
        multi_stmt=False,
        use_lock=True,
        use_cls_lock=False
    )


def __reset_auto_incrment(driver: GoogleMapsTravelTimeMonitor) -> None:
    driverutils.reset_mysql_auto_increment(
        database_name=driver.destination_database_name,
        table_name=driver.destination_table.__tablename__,
        primary_key='id',
        connector=driver.peakdb_connector,
        driver=driver,
        use_lock=True,
    )


def __parse_time_to_minutes(text):
    hours = minutes = 0
    match = re.findall(r'(\d+)\s*(hour|minute|hr|min)', text.lower())
    for value, unit in match:
        if 'hour' in unit or 'hr' in unit:
            hours += int(value)
        elif 'min' in unit:
            minutes += int(value)
    return hours * 60 + minutes
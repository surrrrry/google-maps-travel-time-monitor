#! /usr/bin/env python

from sqlalchemy.orm.decl_api import DeclarativeMeta
from google_maps_travel_time_monitor import table_models
from peaklib.service_driver import ServiceDriver
from google_maps_travel_time_monitor import sql
import google_maps_travel_time_monitor
from peaklib import driverutils
from peaklib import secrets
from peaklib import sqla
from pathlib import Path
from typing import Union
from typing import List
from typing import Type


class GoogleMapsTravelTimeMonitor(ServiceDriver):

    def __init__(self,
                 service_name: Union[str, None] = None,
                 developer_mode_enabled: bool = True,
                 event_logging_enabled: bool = False,
                 query_logging_enabled: bool = False,
                 exception_logging_enabled: bool = False,
                 on_start_enabled: bool = False,
                 heartbeat_enabled: bool = False,
                 discord_service_logging_enabled: bool = False,
                 console_printing_enabled: bool = True,
                 service_software_version: Union[str, None] = None,
                 mysqldb_connector: Union[sqla.SqlAlchemyConnector] = None,
                 peakdb_connector: Union[sqla.SqlAlchemyConnector] = None,
                 secrets_mode: Union[str] = None,
                 secrets_file_path: Union[str, Path, None] = None,
                 heart_beat_interval_seconds: Union[int, float, None] = 60,
                 logging_connector: Union[None, sqla.SqlAlchemyConnector] = None,
                 destination_database_name: Union[None, str] = None,
                 destination_table: Union[None, Type[DeclarativeMeta]] = None,
                 live_loop_interval_unit: Union[None, str] = None,
                 live_loop_interval_value: Union[None, int] = None,
                 rebuild_table: bool = False,
                 enable_chunk_service_function: bool = False,
                 chunk_service_function_chunk_size: int = 1,
                 ):
        super().__init__(
            service_name=service_name,
            developer_mode_enabled=developer_mode_enabled,
            event_logging_enabled=event_logging_enabled,
            query_logging_enabled=query_logging_enabled,
            exception_logging_enabled=exception_logging_enabled,
            on_start_enabled=on_start_enabled,
            heartbeat_enabled=heartbeat_enabled,
            discord_service_logging_enabled=discord_service_logging_enabled,
            console_printing_enabled=console_printing_enabled,
            service_software_version=service_software_version,
            mysqldb_connector=mysqldb_connector,
            peakdb_connector=peakdb_connector,
            secrets_mode=secrets_mode,
            secrets_file_path=secrets_file_path,
            heart_beat_interval_seconds=heart_beat_interval_seconds,
            logging_connector=logging_connector,
            destination_table=destination_table,
            destination_database_name=destination_database_name,
            live_loop_interval_unit=live_loop_interval_unit,
            live_loop_interval_value=live_loop_interval_value,
            rebuild_table=rebuild_table,
            enable_chunk_service_function=enable_chunk_service_function,
            chunk_service_function_chunk_size=chunk_service_function_chunk_size,
        )

        # self.upsert_chunk_size = 100000
        # self.num_upload_threads = 2

    def run_setup(self, verify_connectors: bool = True):
        super(GoogleMapsTravelTimeMonitor, self).run_setup(verify_connectors)

    def setup_database_connectors(self):
        super(GoogleMapsTravelTimeMonitor, self).setup_database_connectors()

        # TODO: ADD MORE CONNECTORS AS NEEDED, BY DEFAULT SURRYDB CONNECTOR IS SET FOR LOGGING VIA SUPER

    def setup_tables(self):
        driverutils.setup_tables(
            rebuild=self.rebuild_table,
            connector=self.mysqldb_connector,
            driver=self,
            database_name=self.destination_database_name,
            table_model=self.destination_table,
        )

    def get_connectors(self, ignore_unset: bool = True) -> List:
        connectors = super(GoogleMapsTravelTimeMonitor, self).get_connectors(ignore_unset)

        # TODO: ADD CONNECTORS

        return connectors

    @staticmethod
    def table_models():
        return table_models

    @staticmethod
    def sql():
        return sql

    def get_google_maps_api_key(self):
        return secrets.load_secret(
            key='google-maps-api-key',
            mode=self.secrets_mode,
            secrets_file_path=self.secrets_file_path
        )['value']


def from_config(fp: Union[str, Path]) -> GoogleMapsTravelTimeMonitor:
    c = driverutils.read_config(fp)
    secrets_fp = driverutils.get_secret_fp_from_config(c)
    return GoogleMapsTravelTimeMonitor(
        secrets_mode=c['mode'],
        secrets_file_path=secrets_fp,
        event_logging_enabled=c['enableEventLogging'],
        heartbeat_enabled=c['enableHeartBeat'],
        developer_mode_enabled=c['developerModeEnabled'],
        service_software_version=google_maps_travel_time_monitor.__version__,
        exception_logging_enabled=c['enableExceptionLogging'],
        query_logging_enabled=c['enabledQueryLogging'],
        on_start_enabled=c['enableOnStart'],
        rebuild_table=c['rebuildTable'],
        live_loop_interval_unit=c['liveLoopIntervalUnit'],
        live_loop_interval_value=c['liveLoopIntervalValue'],
        discord_service_logging_enabled=c['discordServiceLoggingEnabled'],
        enable_chunk_service_function=c['enableChunkServiceFunction'],
        chunk_service_function_chunk_size=c['chunkServiceFunctionChunkSize']
    )



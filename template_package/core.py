#! /usr/bin/env python

from template_package.driver import TemplateDriver
from peaklib import driverutils
from peaklib import mysqlutils
from peaklib import timeutils
from peaklib import logger
from typing import List
import pandas as pd


@logger.service_function()
def run(driver: TemplateDriver, ) -> None:
    pass

    __reset_auto_incrment(driver)


def __extract(queries: List[str], driver: TemplateDriver) -> pd.DataFrame:
    return driverutils.extract(
        driver=driver,
        connector=driver.peakdb_connector,
        target_database_name=driver.source_database_name,
        queries=queries,
        return_as_df=True
    )


@logger.transform_function()
def __transform(df: pd.DataFrame, driver: TemplateDriver) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    odf = df.copy()

    odf['created_at'] = timeutils.get_current_datetime_utc()
    odf['last_updated'] = timeutils.get_current_datetime_utc()

    return df


def __upsert(df: pd.DataFrame, driver: TemplateDriver) -> None:
    if df.empty:
        logger.log_upload_skipped_event(driver=driver)
        return

    stmt = mysqlutils.create_mysql_insert_stmt(
        table_model=driver.destination_table,
        df=df,
        append_ignore=False,
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


def __reset_auto_incrment(driver: TemplateDriver) -> None:
    driverutils.reset_mysql_auto_increment(
        database_name=driver.destination_database_name,
        table_name=driver.destination_table.__tablename__,
        primary_key='id',
        connector=driver.peakdb_connector,
        driver=driver,
        use_lock=True,
    )

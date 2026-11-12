import pandas as pd

from etl.config import get_engine
from etl.logger import get_logger

logger = get_logger(__name__)


def _load_table(df: pd.DataFrame, schema: str, table: str) -> None:
    engine = get_engine()
    logger.info(f"Carregando {len(df):,} linhas em {schema}.{table}")
    df.to_sql(
        table,
        engine,
        schema=schema,
        if_exists="replace",
        index=False,
        chunksize=2000,
        method="multi",
    )
    logger.info(f"{schema}.{table} carregada")


def load_raw(df: pd.DataFrame) -> None:
    _load_table(df, "raw", "hotel_bookings")


def load_staging(df: pd.DataFrame) -> None:
    _load_table(df, "staging", "hotel_bookings")
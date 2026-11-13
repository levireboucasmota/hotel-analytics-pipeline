import pandas as pd

from etl.config import get_engine
from etl.logger import get_logger
from sqlalchemy import text
from etl.config import SQL_DIR, get_engine


logger = get_logger(__name__)


def run_sql_file(filename: str) -> None:
    path = SQL_DIR / filename
    logger.info(f"Executando {path.name}")
    sql = path.read_text(encoding="utf-8-sig")
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text(sql))
    logger.info(f"{path.name} concluído")
    

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
import pandas as pd

from etl.config import RAW_CSV
from etl.logger import get_logger

logger = get_logger(__name__)


def extract_csv(path=RAW_CSV) -> pd.DataFrame:
    logger.info(f"Lendo {path}")
    df = pd.read_csv(path)
    logger.info(f"Extraídas {len(df):,} linhas e {df.shape[1]} colunas")
    return df
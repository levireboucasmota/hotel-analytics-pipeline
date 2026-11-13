import sys

from etl.extract import extract_csv
from etl.load import load_raw, load_staging, run_sql_file
from etl.logger import get_logger
from etl.quality import run_quality_checks
from etl.transform import transform

logger = get_logger(__name__)


def main() -> None:
    logger.info("=== Pipeline iniciado ===")

    run_sql_file("00_create_schemas.sql")
    run_sql_file("01_create_model.sql")

    df_raw = extract_csv()
    load_raw(df_raw)

    df_staging = transform(df_raw)
    load_staging(df_staging)

    run_sql_file("02_load_dimensions.sql")
    run_sql_file("03_load_fact.sql")

    run_quality_checks()

    logger.info("=== Pipeline concluído ===")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Pipeline falhou")
        sys.exit(1)
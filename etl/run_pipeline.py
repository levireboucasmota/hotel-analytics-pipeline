from etl.extract import extract_csv
from etl.load import load_raw, load_staging
from etl.logger import get_logger
from etl.transform import transform

logger = get_logger(__name__)


def main() -> None:
    logger.info("=== Pipeline iniciado ===")

    df_raw = extract_csv()
    load_raw(df_raw)

    df_staging = transform(df_raw)
    load_staging(df_staging)

    logger.info("=== Pipeline concluído ===")


if __name__ == "__main__":
    main()
import pandas as pd

from etl.logger import get_logger

logger = get_logger(__name__)

ADR_OUTLIER_THRESHOLD = 5000

MONTHS = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12,
}

COLUMN_RENAMES = {
    "hotel": "hotel_name",
    "stays_in_weekend_nights": "weekend_nights",
    "stays_in_week_nights": "week_nights",
    "meal": "meal_plan",
    "country": "country_code",
    "reserved_room_type": "reserved_room_code",
    "assigned_room_type": "assigned_room_code",
    "agent": "agent_id",
    "required_car_parking_spaces": "parking_spaces",
    "total_of_special_requests": "special_requests",
}

STAGING_COLUMNS = [
    "hotel_name", "is_canceled", "lead_time", "arrival_date", "booking_date",
    "weekend_nights", "week_nights", "total_nights",
    "adults", "children", "babies",
    "meal_plan", "country_code", "market_segment", "distribution_channel",
    "is_repeated_guest", "previous_cancellations", "previous_bookings_not_canceled",
    "reserved_room_code", "assigned_room_code", "booking_changes", "deposit_type",
    "agent_id", "days_in_waiting_list", "customer_type", "adr",
    "parking_spaces", "special_requests",
    "has_company", "is_adr_zero", "is_zero_nights", "lodging_revenue",
]


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates()
    logger.info(f"Duplicatas removidas: {before - len(df):,}")
    return df


def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df[df["adr"] >= 0]
    logger.info(f"adr negativo removido: {before - len(df):,}")

    before = len(df)
    df = df[df["adr"] < ADR_OUTLIER_THRESHOLD]
    logger.info(f"Outlier de adr removido: {before - len(df):,}")

    before = len(df)
    guests = df["adults"] + df["children"].fillna(0) + df["babies"]
    df = df[guests > 0]
    logger.info(f"Reservas sem hóspedes removidas: {before - len(df):,}")

    return df.copy()


def handle_nulls(df: pd.DataFrame) -> pd.DataFrame:
    df["has_company"] = df["company"].notna().astype(int)
    df = df.drop(columns=["company"])

    df["children"] = df["children"].fillna(0).astype(int)
    df["country"] = df["country"].fillna("Unknown")
    df["agent"] = df["agent"].fillna(0).astype(int)
    return df


def standardize_values(df: pd.DataFrame) -> pd.DataFrame:
    df["meal"] = df["meal"].replace("Undefined", "SC")
    return df


def build_dates(df: pd.DataFrame) -> pd.DataFrame:
    df["arrival_date"] = pd.to_datetime(
        {
            "year": df["arrival_date_year"],
            "month": df["arrival_date_month"].map(MONTHS),
            "day": df["arrival_date_day_of_month"],
        }
    )
    df["booking_date"] = df["arrival_date"] - pd.to_timedelta(df["lead_time"], unit="D")
    return df


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["total_nights"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
    df["lodging_revenue"] = (df["adr"] * df["total_nights"]).round(2)
    df["is_adr_zero"] = (df["adr"] == 0).astype(int)
    df["is_zero_nights"] = (df["total_nights"] == 0).astype(int)
    return df


def transform(df_raw: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Iniciando transformação com {len(df_raw):,} linhas")

    df = df_raw.copy()
    df = remove_duplicates(df)
    df = remove_invalid_rows(df)
    df = handle_nulls(df)
    df = standardize_values(df)
    df = build_dates(df)
    df = add_derived_columns(df)

    df = df.rename(columns=COLUMN_RENAMES)[STAGING_COLUMNS]

    logger.info(f"Transformação concluída: {len(df):,} linhas, {df.shape[1]} colunas")
    return df
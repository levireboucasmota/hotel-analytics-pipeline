import numpy as np
import pandas as pd

from etl.transform import STAGING_COLUMNS, transform

BASE_ROW = {
    "hotel": "City Hotel",
    "is_canceled": 0,
    "lead_time": 10,
    "arrival_date_year": 2016,
    "arrival_date_month": "July",
    "arrival_date_week_number": 29,
    "arrival_date_day_of_month": 15,
    "stays_in_weekend_nights": 1,
    "stays_in_week_nights": 2,
    "adults": 2,
    "children": 0.0,
    "babies": 0,
    "meal": "BB",
    "country": "PRT",
    "market_segment": "Online TA",
    "distribution_channel": "TA/TO",
    "is_repeated_guest": 0,
    "previous_cancellations": 0,
    "previous_bookings_not_canceled": 0,
    "reserved_room_type": "A",
    "assigned_room_type": "A",
    "booking_changes": 0,
    "deposit_type": "No Deposit",
    "agent": 9.0,
    "company": np.nan,
    "days_in_waiting_list": 0,
    "customer_type": "Transient",
    "adr": 100.0,
    "required_car_parking_spaces": 0,
    "total_of_special_requests": 0,
    "reservation_status": "Check-Out",
    "reservation_status_date": "2016-07-18",
}


def make_df(*overrides: dict) -> pd.DataFrame:
    """Monta um DataFrame com as colunas do CSV original. Cada dict sobrescreve a linha base."""
    rows = [{**BASE_ROW, **o} for o in (overrides or ({},))]
    return pd.DataFrame(rows)


def test_removes_duplicates():
    result = transform(make_df({}, {}))
    assert len(result) == 1


def test_removes_negative_adr():
    result = transform(make_df({}, {"adr": -1.0}))
    assert len(result) == 1
    assert (result["adr"] >= 0).all()


def test_removes_adr_outlier():
    result = transform(make_df({}, {"adr": 5400.0}))
    assert len(result) == 1


def test_removes_bookings_without_guests():
    result = transform(make_df({}, {"adults": 0, "children": 0.0, "babies": 0}))
    assert len(result) == 1


def test_fills_nulls():
    result = transform(make_df({"country": None, "agent": np.nan, "children": np.nan}))
    row = result.iloc[0]
    assert row["country_code"] == "Unknown"
    assert row["agent_id"] == 0
    assert row["children"] == 0


def test_company_becomes_flag():
    result = transform(make_df({"company": 223.0}, {"company": np.nan, "lead_time": 11}))
    flags = dict(zip(result["lead_time"], result["has_company"]))
    assert flags[10] == 1
    assert flags[11] == 0
    assert "company" not in result.columns


def test_standardizes_meal():
    result = transform(make_df({"meal": "Undefined"}))
    assert result.iloc[0]["meal_plan"] == "SC"


def test_builds_booking_date_from_lead_time():
    result = transform(make_df({"lead_time": 10}))
    row = result.iloc[0]
    assert row["arrival_date"] == pd.Timestamp("2016-07-15")
    assert row["booking_date"] == pd.Timestamp("2016-07-05")


def test_derived_columns():
    result = transform(make_df({"adr": 100.0, "stays_in_weekend_nights": 1, "stays_in_week_nights": 2}))
    row = result.iloc[0]
    assert row["total_nights"] == 3
    assert row["lodging_revenue"] == 300.0
    assert row["is_adr_zero"] == 0


def test_keeps_adr_zero_and_zero_night_rows_with_flags():
    result = transform(make_df({"adr": 0.0, "stays_in_weekend_nights": 0, "stays_in_week_nights": 0}))
    assert len(result) == 1
    row = result.iloc[0]
    assert row["is_adr_zero"] == 1
    assert row["is_zero_nights"] == 1


def test_output_has_expected_columns():
    result = transform(make_df())
    assert list(result.columns) == STAGING_COLUMNS
    assert "reservation_status" not in result.columns


def test_does_not_modify_input():
    df = make_df({"country": None})
    snapshot = df.copy()
    transform(df)
    pd.testing.assert_frame_equal(df, snapshot)
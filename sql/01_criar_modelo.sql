CREATE TABLE IF NOT EXISTS mart.dim_hotel (
    hotel_key   SERIAL PRIMARY KEY,
    hotel_name  VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS mart.dim_channel (
    channel_key          SERIAL PRIMARY KEY,
    market_segment       VARCHAR(50) NOT NULL,
    distribution_channel VARCHAR(50) NOT NULL,
    UNIQUE (market_segment, distribution_channel)
);

CREATE TABLE IF NOT EXISTS mart.dim_date (
    date_key      INT PRIMARY KEY,
    full_date     DATE NOT NULL UNIQUE,
    year          INT NOT NULL,
    month         INT NOT NULL,
    month_name    VARCHAR(20) NOT NULL,
    quarter       INT NOT NULL,
    week_of_year  INT NOT NULL,
    day_of_week   INT NOT NULL,
    day_name      VARCHAR(20) NOT NULL,
    is_weekend    SMALLINT NOT NULL
);

CREATE TABLE IF NOT EXISTS mart.dim_booking_profile (
    profile_key    SERIAL PRIMARY KEY,
    meal_plan      VARCHAR(50) NOT NULL,
    deposit_type   VARCHAR(50) NOT NULL,
    customer_type  VARCHAR(50) NOT NULL,
    UNIQUE (meal_plan, deposit_type, customer_type)
);

CREATE TABLE IF NOT EXISTS mart.dim_country (
    country_key   SERIAL PRIMARY KEY,
    country_code  VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS mart.dim_room_type (
    room_type_key  SERIAL PRIMARY KEY,
    room_code      VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS mart.fact_booking (
    booking_key             SERIAL PRIMARY KEY,
    arrival_date_key        INT NOT NULL REFERENCES mart.dim_date(date_key),
    booking_date_key        INT NOT NULL REFERENCES mart.dim_date(date_key),
    hotel_key               INT NOT NULL REFERENCES mart.dim_hotel(hotel_key),
    channel_key             INT NOT NULL REFERENCES mart.dim_channel(channel_key),
    country_key             INT NOT NULL REFERENCES mart.dim_country(country_key),
    reserved_room_type_key  INT NOT NULL REFERENCES mart.dim_room_type(room_type_key),
    assigned_room_type_key  INT NOT NULL REFERENCES mart.dim_room_type(room_type_key),
    profile_key             INT NOT NULL REFERENCES mart.dim_booking_profile(profile_key),
    agent_id                INT NOT NULL,     -- 0 = no agent
    lead_time               INT NOT NULL,
    weekend_nights          INT NOT NULL,
    week_nights             INT NOT NULL,
    total_nights            INT NOT NULL,
    adults                  INT NOT NULL,
    children                INT NOT NULL,
    babies                  INT NOT NULL,
    adr                     NUMERIC(10, 2) NOT NULL,
    lodging_revenue         NUMERIC(12, 2) NOT NULL,
    is_canceled             SMALLINT NOT NULL,
    is_repeated_guest       SMALLINT NOT NULL,
    is_adr_zero             SMALLINT NOT NULL,
    is_zero_nights          SMALLINT NOT NULL,
    has_company             SMALLINT NOT NULL,
    booking_changes         INT NOT NULL,
    days_in_waiting_list    INT NOT NULL,
    special_requests        INT NOT NULL,
    parking_spaces          INT NOT NULL,
    previous_cancellations  INT NOT NULL
);
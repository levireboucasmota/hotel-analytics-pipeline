from dataclasses import dataclass

from sqlalchemy import text

from etl.config import get_engine
from etl.logger import get_logger

logger = get_logger(__name__)


class DataQualityError(Exception):
    """Levantada quando uma verificação crítica falha."""


@dataclass(frozen=True)
class Check:
    name: str
    sql: str
    expected: int = 0
    severity: str = "error"   # "error" interrompe o pipeline; "warning" só avisa


CHECKS = [
    # --- Completude: nada se perdeu entre as camadas ---
    Check(
        "fato tem o mesmo número de linhas que o staging",
        "SELECT (SELECT COUNT(*) FROM staging.hotel_bookings)"
        " - (SELECT COUNT(*) FROM mart.fact_booking)",
    ),
    Check(
        "staging não tem mais linhas que o raw",
        "SELECT CASE WHEN (SELECT COUNT(*) FROM staging.hotel_bookings)"
        " <= (SELECT COUNT(*) FROM raw.hotel_bookings) THEN 0 ELSE 1 END",
    ),
    Check("dim_date cobre 2013-2017 (1826 dias)", "SELECT COUNT(*) FROM mart.dim_date", expected=1826),
    Check("dim_hotel tem 2 hoteis", "SELECT COUNT(*) FROM mart.dim_hotel", expected=2),

    # --- Validade: valores dentro do que faz sentido ---
    Check("adr negativo", "SELECT COUNT(*) FROM mart.fact_booking WHERE adr < 0"),
    Check("adr acima do limite de outlier", "SELECT COUNT(*) FROM mart.fact_booking WHERE adr >= 5000"),
    Check(
        "reservas sem hospedes",
        "SELECT COUNT(*) FROM mart.fact_booking WHERE adults + children + babies = 0",
    ),
    Check("lead_time negativo", "SELECT COUNT(*) FROM mart.fact_booking WHERE lead_time < 0"),
    Check("agent_id negativo", "SELECT COUNT(*) FROM mart.fact_booking WHERE agent_id < 0"),
    Check(
        "flags fora de 0/1",
        "SELECT COUNT(*) FROM mart.fact_booking WHERE is_canceled NOT IN (0, 1)"
        " OR is_repeated_guest NOT IN (0, 1) OR is_adr_zero NOT IN (0, 1)"
        " OR is_zero_nights NOT IN (0, 1) OR has_company NOT IN (0, 1)",
    ),

    # --- Consistência: colunas que se relacionam entre si ---
    Check(
        "total_nights diferente de weekend_nights + week_nights",
        "SELECT COUNT(*) FROM mart.fact_booking WHERE total_nights <> weekend_nights + week_nights",
    ),
    Check(
        "lodging_revenue diferente de adr * total_nights",
        "SELECT COUNT(*) FROM mart.fact_booking"
        " WHERE ABS(lodging_revenue - adr * total_nights) > 0.01",
    ),
    Check(
        "data da reserva posterior a data de chegada",
        "SELECT COUNT(*) FROM mart.fact_booking f"
        " JOIN mart.dim_date a ON a.date_key = f.arrival_date_key"
        " JOIN mart.dim_date b ON b.date_key = f.booking_date_key"
        " WHERE b.full_date > a.full_date",
    ),
    Check(
        "chegadas fora do periodo do dataset (jul/2015 a ago/2017)",
        "SELECT COUNT(*) FROM mart.fact_booking f"
        " JOIN mart.dim_date a ON a.date_key = f.arrival_date_key"
        " WHERE a.full_date NOT BETWEEN '2015-07-01' AND '2017-08-31'",
    ),

    # --- Plausibilidade: alerta, mas não interrompe ---
    Check(
        "taxa de cancelamento fora da faixa esperada (15% a 50%)",
        "SELECT CASE WHEN AVG(is_canceled) BETWEEN 0.15 AND 0.50 THEN 0 ELSE 1 END"
        " FROM mart.fact_booking",
        severity="warning",
    ),
]


def run_quality_checks() -> None:
    logger.info(f"Executando {len(CHECKS)} verificações de qualidade")
    failures = []

    with get_engine().connect() as conn:
        for check in CHECKS:
            value = conn.execute(text(check.sql)).scalar()
            if value == check.expected:
                logger.info(f"[PASS] {check.name}")
            elif check.severity == "warning":
                logger.warning(f"[WARN] {check.name}: obtido {value}, esperado {check.expected}")
            else:
                logger.error(f"[FAIL] {check.name}: obtido {value}, esperado {check.expected}")
                failures.append(check.name)

    if failures:
        raise DataQualityError(f"{len(failures)} verificação(ões) falharam: {failures}")

    logger.info("Todas as verificações críticas passaram")
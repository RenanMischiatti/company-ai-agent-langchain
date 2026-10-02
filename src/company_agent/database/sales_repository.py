from dataclasses import dataclass
from decimal import Decimal

from company_agent.config import Settings
from company_agent.database.connection import create_database_connection


@dataclass(frozen=True)
class SalesSummary:
    count: int
    total: Decimal
    average: Decimal


class SalesRepository:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def summarize(self, year: int, month: int | None) -> SalesSummary:
        conditions = [
            "status = 'completed'",
            "EXTRACT(YEAR FROM sold_at) = %s",
        ]
        parameters: list[int] = [year]

        if month is not None:
            conditions.append("EXTRACT(MONTH FROM sold_at) = %s")
            parameters.append(month)

        query = f"""
            SELECT
                COUNT(*) AS count,
                COALESCE(SUM(amount), 0) AS total,
                COALESCE(AVG(amount), 0) AS average
            FROM sales
            WHERE {' AND '.join(conditions)}
        """

        with create_database_connection(self._settings) as connection:
            row = connection.execute(query, parameters).fetchone()

        if row is None:
            return SalesSummary(0, Decimal("0"), Decimal("0"))

        return SalesSummary(
            count=int(row[0]),
            total=Decimal(row[1]),
            average=Decimal(row[2]),
        )

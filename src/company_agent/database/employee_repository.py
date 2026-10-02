from dataclasses import dataclass

from company_agent.config import Settings
from company_agent.database.connection import create_database_connection


@dataclass(frozen=True)
class EmployeeRecord:
    name: str
    department: str
    role: str
    active: bool


class EmployeeRepository:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def find(
        self,
        department: str | None,
        active_only: bool,
    ) -> list[EmployeeRecord]:
        conditions: list[str] = []
        parameters: list[object] = []

        if department is not None:
            conditions.append("LOWER(department) = LOWER(%s)")
            parameters.append(department)

        if active_only:
            conditions.append("active = TRUE")

        where_clause = ""
        if conditions:
            where_clause = f"WHERE {' AND '.join(conditions)}"

        query = f"""
            SELECT name, department, role, active
            FROM employees
            {where_clause}
            ORDER BY name
        """

        with create_database_connection(self._settings) as connection:
            rows = connection.execute(query, parameters).fetchall()

        return [
            EmployeeRecord(
                name=str(row[0]),
                department=str(row[1]),
                role=str(row[2]),
                active=bool(row[3]),
            )
            for row in rows
        ]

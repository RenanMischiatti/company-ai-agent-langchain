from langchain.tools import tool
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from company_agent.database.employee_repository import EmployeeRepository
from company_agent.database.sales_repository import SalesRepository


MONTH_NAMES = {
    1: "janeiro",
    2: "fevereiro",
    3: "marco",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro",
}


class SalesQueryInput(BaseModel):
    year: int = Field(description="Ano da venda com quatro digitos.")
    month: int | None = Field(
        default=None,
        ge=1,
        le=12,
        description="Numero do mes de 1 a 12; use null para o ano inteiro.",
    )


class EmployeeQueryInput(BaseModel):
    department: str | None = Field(
        default=None,
        description="Departamento solicitado; use null para todos.",
    )
    active_only: bool = Field(
        default=True,
        description="Se true, retorna somente funcionarios ativos.",
    )


def create_sales_query_tool(repository: SalesRepository) -> BaseTool:
    @tool(args_schema=SalesQueryInput, return_direct=True)
    def query_sales(year: int, month: int | None = None) -> str:
        """Consulta quantidade, valor total e ticket medio de vendas concluidas."""
        summary = repository.summarize(year=year, month=month)
        period = str(year)
        if month is not None:
            period = f"{MONTH_NAMES[month]} de {year}"

        return (
            f"Vendas concluidas em {period}: {summary.count}. "
            f"Valor total: R$ {summary.total:.2f}. "
            f"Ticket medio: R$ {summary.average:.2f}."
        )

    return query_sales


def create_employee_query_tool(repository: EmployeeRepository) -> BaseTool:
    @tool(args_schema=EmployeeQueryInput, return_direct=True)
    def query_employees(
        department: str | None = None,
        active_only: bool = True,
    ) -> str:
        """Consulta funcionarios por departamento e situacao ativa ou inativa."""
        employees = repository.find(
            department=department,
            active_only=active_only,
        )

        if not employees:
            return "Nenhum funcionario encontrado para os filtros informados."

        lines = [
            f"{employee.name} | {employee.department} | {employee.role} | "
            f"{'ativo' if employee.active else 'inativo'}"
            for employee in employees
        ]
        return "\n".join(lines)

    return query_employees

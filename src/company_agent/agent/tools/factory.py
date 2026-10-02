from langchain_core.tools import BaseTool

from company_agent.config import Settings
from company_agent.database.employee_repository import EmployeeRepository
from company_agent.database.sales_repository import SalesRepository
from company_agent.rag.factory import create_rag_service
from company_agent.agent.tools.database_query import (
    create_employee_query_tool,
    create_sales_query_tool,
)
from company_agent.agent.tools.document_search import create_document_search_tool


def create_agent_tools(settings: Settings) -> list[BaseTool]:
    rag_service = create_rag_service(settings)
    sales_repository = SalesRepository(settings)
    employee_repository = EmployeeRepository(settings)

    return [
        create_document_search_tool(rag_service),
        create_sales_query_tool(sales_repository),
        create_employee_query_tool(employee_repository),
    ]

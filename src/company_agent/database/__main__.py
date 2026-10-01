from company_agent.config import load_settings
from company_agent.database.schema import initialize_database


if __name__ == "__main__":
    initialize_database(load_settings())
    print("Banco de dados inicializado com sucesso.")

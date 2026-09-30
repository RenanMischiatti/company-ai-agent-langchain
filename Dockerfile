FROM python:3.12-slim

# Evita arquivos .pyc e faz os logs aparecerem imediatamente no terminal.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copiar as dependencias antes do codigo aproveita o cache de camadas do Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY src ./src

CMD ["python", "-m", "company_agent"]

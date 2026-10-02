# Company AI Agent com LangChain

Projeto de estudo que demonstra a construção de um agente empresarial com Python e LangChain.

O agente recebe uma pergunta e decide se deve:

- responder diretamente com o modelo;
- pesquisar políticas e informações internas usando RAG;
- consultar dados estruturados de vendas e funcionários no PostgreSQL;
- futuramente, consultar uma API externa.

Todo o ambiente roda com Docker Compose. Não é necessário instalar Python, PostgreSQL ou Ollama no Windows.

## Tecnologias

- Python 3.12;
- LangChain;
- Ollama com `llama3.2:3b`;
- Ollama Embeddings com `nomic-embed-text-v2-moe`;
- PostgreSQL 16;
- pgvector;
- Docker Compose.

## Como o projeto funciona

```text
Pergunta do usuário
        |
        v
  Agente LangChain
        |
        +-- responde diretamente
        |
        +-- tool de documentos --> RAG --> pgvector
        |
        `-- tool de banco ------> repositories --> PostgreSQL
```

O modelo escolhe uma tool observando o nome, a descrição e os parâmetros disponíveis. As tools não possuem as regras de acesso aos dados: elas delegam o trabalho para o `RagService` ou para os repositories.

## Pré-requisito

- Docker Desktop aberto e em execução.

## Setup rápido

Execute os comandos abaixo na raiz do projeto.

### 1. Criar o arquivo de configuração

No PowerShell:

```powershell
Copy-Item .env.example .env
```

No Git Bash, WSL ou Linux:

```bash
cp .env.example .env
```

Para estudar localmente, os valores padrão do `.env.example` já são suficientes. Não envie um `.env` contendo credenciais reais para o GitHub.

### 2. Construir e iniciar o ambiente

```bash
docker compose up --build -d
```

Esse comando:

- constrói o container Python `app`;
- inicia o Ollama dentro do Docker;
- baixa o modelo de chat e o modelo de embeddings;
- inicia PostgreSQL com pgvector;
- mantém o container `app` ativo para receber comandos.

Na primeira execução, o download dos modelos pode levar alguns minutos. Os modelos e o banco ficam em volumes Docker e não são baixados novamente a cada inicialização.

Confira os containers:

```bash
docker compose ps
```

### 3. Inicializar e popular o banco

```bash
docker compose exec app python -m company_agent.database
```

Esse módulo:

- habilita a extensão `vector`;
- cria `documents` e `document_chunks` para o RAG;
- recria `employees` e `sales`;
- insere 50 funcionários e 600 vendas fictícias.

Os IDs de funcionários e vendas são inteiros sequenciais. Executar esse comando novamente reinicia somente os dados fictícios de `employees` e `sales`; os documentos e embeddings já indexados são preservados.

### 4. Indexar os documentos internos

Os arquivos `.txt` usados pelo RAG ficam em:

```text
data/documents/
```

Para gerar chunks e embeddings:

```bash
docker compose exec app python -m company_agent.rag
```

Esse módulo:

1. carrega os arquivos `.txt`;
2. separa o conteúdo por seções;
3. divide seções grandes em chunks;
4. gera embeddings com o Ollama;
5. grava os textos, metadados e vetores no PostgreSQL.

Execute novamente quando adicionar ou alterar documentos.

### 5. Fazer uma pergunta ao agente

```bash
docker compose exec app python -m company_agent "Quantas vendas concluídas tivemos em junho de 2026?"
```

Outros exemplos:

```bash
docker compose exec app python -m company_agent "Quais funcionários ativos trabalham em Vendas?"

docker compose exec app python -m company_agent "Segundo os documentos internos, como funciona o trabalho remoto?"

docker compose exec app python -m company_agent "Qual é a capital do Brasil?"
```

A pergunta sobre vendas usa a tool de vendas; a pergunta sobre funcionários usa a tool de funcionários; e a pergunta sobre trabalho remoto pesquisa o RAG. Uma pergunta de conhecimento geral, como a da capital do Brasil, pode ser respondida diretamente pelo modelo.

## Trabalhar dentro do container

O serviço `app` permanece ativo. Se preferir abrir um terminal dentro dele:

```bash
docker compose exec app bash
```

Depois, os comandos ficam menores:

```bash
python -m company_agent.database
python -m company_agent.rag
python -m company_agent "Sua pergunta"
```

Use `exit` para sair do container.

## Comandos principais

| Objetivo | Comando |
|---|---|
| Subir o projeto | `docker compose up --build -d` |
| Ver os serviços | `docker compose ps` |
| Abrir o container Python | `docker compose exec app bash` |
| Inicializar e popular o banco | `docker compose exec app python -m company_agent.database` |
| Indexar documentos | `docker compose exec app python -m company_agent.rag` |
| Perguntar ao agente | `docker compose exec app python -m company_agent "Pergunta"` |
| Ver ajuda da CLI | `docker compose exec app python -m company_agent --help` |
| Listar modelos Ollama | `docker compose exec ollama ollama list` |
| Ver logs | `docker compose logs -f` |
| Parar os containers | `docker compose down` |

`docker compose down` preserva os volumes. Para o uso normal do projeto, não utilize `docker compose down -v`, pois a opção `-v` também apaga o banco e os modelos baixados.

## Módulos executáveis do setup

Os três comandos Python principais usam o `-m`, que manda o Python executar um pacote como programa:

| Módulo | Arquivo de entrada | Responsabilidade |
|---|---|---|
| `company_agent.database` | `database/__main__.py` | Cria o schema e executa o seed |
| `company_agent.rag` | `rag/__main__.py` | Processa e indexa os documentos |
| `company_agent` | `company_agent/__main__.py` | Recebe a pergunta e inicia o agente |

Por isso executamos `python -m company_agent.rag`, e não precisamos informar o caminho completo de um arquivo `.py`.

## Configuração do `.env`

As principais variáveis são:

| Variável | Uso |
|---|---|
| `OLLAMA_MODEL` | Modelo usado pelo agente |
| `OLLAMA_EMBEDDING_MODEL` | Modelo que transforma textos em vetores |
| `POSTGRES_USER` | Usuário do PostgreSQL |
| `POSTGRES_PASSWORD` | Senha do PostgreSQL |
| `POSTGRES_DB` | Nome do banco |
| `DATABASE_URL` | Conexão usada pela aplicação |
| `RAG_DOCUMENTS_PATH` | Diretório de documentos dentro do container |
| `RAG_CHUNK_SIZE` | Tamanho máximo aproximado dos chunks |
| `RAG_CHUNK_OVERLAP` | Sobreposição entre chunks |
| `RAG_TOP_K` | Quantidade de chunks recuperados por pesquisa |

Ao alterar `OLLAMA_MODEL` ou `OLLAMA_EMBEDDING_MODEL`, execute novamente `docker compose up -d` para que o Compose baixe o modelo configurado.

## Conectar pelo DBeaver

O PostgreSQL é publicado somente no computador local:

| Campo | Valor padrão |
|---|---|
| Host | `127.0.0.1` |
| Porta | `5433` |
| Database | valor de `POSTGRES_DB` |
| Usuário | valor de `POSTGRES_USER` |
| Senha | valor de `POSTGRES_PASSWORD` |

Os containers usam internamente a porta `5432`; o DBeaver no Windows deve usar a porta `5433`.

## Arquitetura de pastas

```text
.
|-- data/
|   `-- documents/                 # Arquivos .txt usados pelo RAG
|-- .env.example                   # Exemplo das configurações
|-- compose.yaml                   # Serviços app, Ollama e PostgreSQL
|-- Dockerfile                     # Imagem Python da aplicação
|-- requirements.txt               # Dependências Python
`-- src/
    `-- company_agent/
        |-- __main__.py             # Entrada: python -m company_agent
        |-- bootstrap.py            # Composition Root da aplicação
        |-- cli.py                  # Leitura dos argumentos da CLI
        |-- config.py               # Carregamento das configurações
        |-- main.py                 # Fluxo principal
        |-- agent/
        |   |-- company_agent.py    # Encapsula o agente LangChain
        |   |-- prompts.py          # Instruções do agente
        |   `-- tools/
        |       |-- factory.py      # Monta as tools e dependências
        |       |-- database_query.py
        |       `-- document_search.py
        |-- database/
        |   |-- __main__.py         # Entrada do setup do banco
        |   |-- schema.py           # Executa os arquivos SQL
        |   |-- schema.sql          # Estrutura das tabelas
        |   |-- seed.sql            # Dados fictícios
        |   `-- *_repository.py     # Consultas ao PostgreSQL
        |-- llm/
        |   `-- ollama.py           # Criação do modelo de chat
        `-- rag/
            |-- __main__.py         # Entrada da indexação
            |-- factory.py          # Monta o serviço de RAG
            |-- ingestion.py        # Coordena a indexação
            |-- section_splitter.py # Divide documentos em chunks
            |-- embeddings.py       # Cria o modelo de embeddings
            |-- vector_store.py     # Integração com pgvector
            `-- rag_service.py      # Pesquisa os documentos
```

### Responsabilidades

- `bootstrap.py` é a **Composition Root**: conecta modelo, configurações e tools.
- `agent/tools/factory.py` usa o padrão **Factory** para montar as tools.
- `rag/factory.py` esconde os detalhes de embeddings, engine e vector store.
- repositories concentram as consultas SQL e não dependem do agente.
- tools adaptam os serviços da aplicação para o formato entendido pelo LangChain.

Essa separação permite trocar o banco, o modelo ou a implementação do RAG sem colocar toda a configuração dentro do `main.py`.

## Serviços Docker

- `app`: ambiente Python onde o projeto é executado;
- `ollama`: servidor local dos modelos;
- `ollama-pull-chat`: baixa o modelo de chat durante o `docker compose up`;
- `ollama-pull-embedding`: baixa o modelo de embeddings;
- `postgres`: banco PostgreSQL com pgvector.

Dentro da rede Docker, a aplicação acessa Ollama por `http://ollama:11434` e PostgreSQL por `postgres:5432`. Esses nomes são resolvidos pelo próprio Docker Compose.

## Reiniciar o projeto depois do primeiro setup

Como banco e modelos ficam persistidos, nas próximas vezes normalmente basta:

```bash
docker compose up -d
docker compose exec app python -m company_agent "Sua pergunta"
```

Não é necessário executar o initializer ou a indexação novamente, exceto quando você quiser recriar os dados fictícios ou atualizar os documentos.

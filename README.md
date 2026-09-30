# Company AI Agent com LangChain

Projeto de estudo para construir, passo a passo, um agente empresarial capaz de escolher entre:

- consultar documentos internos com RAG;
- consultar um banco de dados por meio de tools;
- chamar uma API externa.

Nesta primeira etapa, o projeto possui um ambiente Python em Docker, um container do Ollama, configuracoes por variaveis de ambiente e uma aplicacao LangChain que envia uma mensagem inicial ao modelo.

## Pre-requisitos

- Docker Desktop em execucao.

## Executar

Na raiz do projeto, construa e inicie os containers em segundo plano:

```bash
docker compose up --build -d
```

Na primeira execucao, o Compose tambem baixa automaticamente o modelo `llama3.2:3b`. O container `app` inicia depois que o download termina. Nas proximas execucoes, o modelo ja estara no volume persistente e essa verificacao sera mais rapida.

O container `app` fica ativo para funcionar como ambiente de desenvolvimento. Entre nele com:

```bash
docker compose exec app bash
```

Dentro do container, execute:

```bash
python -m company_agent "Qual e a capital do Brasil?"
```

A pergunta e recebida pela interface de linha de comando e encaminhada ao agente. O agente pode responder diretamente ou chamar as tools simuladas de documentos internos e banco de dados. Para ver a ajuda do comando, execute `python -m company_agent --help`.

Digite `exit` para sair do terminal do container.

## Ollama

O Ollama roda no servico `ollama`, sem precisar ser instalado no Windows. O servico auxiliar `ollama-pull` instala automaticamente o modelo configurado durante o `docker compose up`.

Se quiser baixar outro modelo manualmente no futuro, use, por exemplo:

```bash
docker compose exec ollama ollama pull llama3.2:3b
```

Liste os modelos instalados:

```bash
docker compose exec ollama ollama list
```

Os modelos ficam no volume Docker `ollama_data`, portanto nao sao baixados novamente sempre que os containers forem recriados.

Para encerrar os containers:

```bash
docker compose down
```

## Estrutura inicial

```text
.
|-- .env.example
|-- Dockerfile
|-- compose.yaml
|-- requirements.txt
`-- src/
    `-- company_agent/
        |-- __init__.py
        |-- __main__.py
        |-- bootstrap.py
        |-- cli.py
        |-- config.py
        |-- main.py
        |-- agent/
        |   |-- __init__.py
        |   |-- company_agent.py
        |   `-- prompts.py
        |-- llm/
        |   |-- __init__.py
        |   `-- ollama.py
        `-- tools/
            |-- __init__.py
            |-- database_query.py
            `-- document_search.py
```

Dentro da rede criada pelo Compose, a aplicacao acessa o Ollama pelo endereco `http://ollama:11434`. O nome do servico, `ollama`, funciona como hostname interno.
Essa porta nao e publicada no Windows: a API fica acessivel somente para os containers da rede do projeto.

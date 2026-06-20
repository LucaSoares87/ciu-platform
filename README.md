# Central de Inteligência Urbana (CIU)

Este repositório contém a estrutura inicial do projeto **Central de Inteligência Urbana (CIU)**.  
Ele foi pensado como ponto de partida para a Fase 1 (Cidade Observável) e inclui um backend em **FastAPI**, um banco de dados **PostgreSQL** com extensão **PostGIS** e um frontend em **React** (não incluso neste commit).  

O objetivo desta etapa é disponibilizar uma API e um modelo de banco de dados capaz de registrar cruzamentos monitorados, suas câmeras associadas e as observações de tráfego (contagens de veículos, filas etc.).  

## Estrutura de diretórios

```
ciu-platform/
│
├── backend/
│   ├── app/
│   │   ├── api/             # Rotas da API
│   │   │   └── v1/
│   │   │       └── routes.py
│   │   ├── core/            # Configurações e inicialização
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── models/          # Modelos do SQLAlchemy
│   │   │   └── __init__.py
│   │   ├── schemas/         # Esquemas Pydantic para validação
│   │   │   └── __init__.py
│   │   ├── crud/            # Funções de acesso ao banco
│   │   │   └── __init__.py
│   │   ├── main.py          # Ponto de entrada da aplicação FastAPI
│   │   └── seed.py          # Script opcional para popular alguns dados
│   │
│   ├── alembic/             # Diretório reservado para migrações
│   │   └── README
│   ├── Dockerfile           # Dockerfile do backend
│   ├── requirements.txt     # Dependências Python
│   └── .env.example         # Variáveis de ambiente de exemplo
│
├── docker-compose.yml       # Orquestração de serviços (DB + backend)
└── docs/
    ├── arquitetura.md       # Documentação da arquitetura geral
    └── banco.md             # Descrição das tabelas e relacionamentos
```

Para instruções detalhadas de execução local e explicações, consulte os arquivos em `docs/`.
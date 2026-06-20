from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings


# Cria o motor de conexão utilizando a URL fornecida nas configurações
engine = create_engine(settings.database_url, echo=False, future=True)

# Classe base para os modelos ORM
Base = declarative_base()

# Sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Provedor de dependência que gera uma nova sessão para cada requisição."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
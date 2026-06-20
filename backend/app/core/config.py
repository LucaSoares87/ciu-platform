import os
from pydantic import BaseModel


class Settings(BaseModel):
    """Configurações da aplicação carregadas de variáveis de ambiente."""
    database_url: str = os.getenv("DATABASE_URL", "postgresql://ciu:ciupassword@localhost:5432/ciu")

    class Config:
        extra = "ignore"


settings = Settings()
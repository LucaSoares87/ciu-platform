from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.database import Base, engine
from .api.v1.routes import router as api_router

# Cria as tabelas no banco ao iniciar o app (somente em ambiente de dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Central de Inteligência Urbana", version="0.1.0")

# Configuração básica de CORS para permitir acesso ao frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas da API versão 1
app.include_router(api_router, prefix="/api/v1")
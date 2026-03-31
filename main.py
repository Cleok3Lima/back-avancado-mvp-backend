# main.py
# Ponto de entrada da aplicação FastAPI

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import diario, episodios

# Cria todas as tabelas no banco de dados (se ainda não existirem)
# Isso executa ao iniciar o servidor pela primeira vez
Base.metadata.create_all(bind=engine)

# Instância principal da aplicação FastAPI
app = FastAPI(
    title="Diário de Episódios — Rick & Morty API",
    description=(
        "API REST para o diário pessoal de episódios de Rick and Morty. "
        "Permite criar, visualizar, editar e deletar anotações e avaliações por episódio. "
        "Também consome a API pública do Rick and Morty para listar episódios e personagens."
    ),
    version="1.0.0",
)

# Configuração do CORS — permite que o frontend React acesse a API
# Em produção, substitua allow_origins por uma lista específica de domínios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Permite qualquer origem (ideal para desenvolvimento)
    allow_credentials=True,
    allow_methods=["*"],        # Permite todos os métodos HTTP (GET, POST, PUT, DELETE...)
    allow_headers=["*"],        # Permite todos os cabeçalhos
)

# Registra os roteadores com seus respectivos prefixos
app.include_router(diario.router)
app.include_router(episodios.router)


@app.get("/", tags=["Root"], summary="Health check")
def root():
    """Endpoint raiz para verificar se a API está no ar."""
    return {"status": "ok", "message": "Diário de Episódios — Rick & Morty API está rodando!"}

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Garante que o diretório ./data exista antes de criar o banco
# Isso é necessário para que o volume do Docker Compose funcione corretamente
os.makedirs("./data", exist_ok=True)

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/diario.db"

# check_same_thread=False é necessário para o SQLite funcionar com FastAPI (multithreaded)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency do FastAPI que fornece uma sessão de banco de dados por requisição.
    O bloco finally garante que a sessão seja fechada mesmo em caso de erro.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

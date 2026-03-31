# database.py
# Configuração do banco de dados SQLite com SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão com o banco SQLite — cria o arquivo diario.db na raiz do projeto
SQLALCHEMY_DATABASE_URL = "sqlite:///./diario.db"

# Engine: responsável pela conexão com o banco
# check_same_thread=False é necessário para o SQLite funcionar com FastAPI (que é assíncrono)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# SessionLocal: fábrica de sessões — cada requisição abre e fecha a sua própria sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: classe base da qual todos os modelos ORM vão herdar
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

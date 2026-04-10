from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class DiarioEntry(Base):
    """
    Modelo que representa uma entrada no diário pessoal de episódios.
    Cada entrada corresponde a um episódio da série Rick and Morty
    e contém a nota (texto) e avaliação (estrelas) do usuário.
    """

    __tablename__ = "diario"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    episode_id = Column(Integer, nullable=False)
    # Nome armazenado localmente para evitar chamadas à API externa na listagem
    episode_name = Column(String, nullable=False)
    nota = Column(String, nullable=True)
    avaliacao = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # nullable=True para compatibilidade com entradas criadas antes do sistema de autenticação
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="entries")


class User(Base):
    """
    Modelo que representa um usuário cadastrado na aplicação.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    entries = relationship("DiarioEntry", back_populates="user")

# models.py
# Definição dos modelos ORM (mapeamento objeto-relacional com SQLAlchemy)

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class DiarioEntry(Base):
    """
    Modelo que representa uma entrada no diário pessoal de episódios.
    Cada entrada corresponde a um episódio da série Rick and Morty
    e contém a nota (texto) e avaliação (estrelas) do usuário.
    """

    __tablename__ = "diario"

    # Chave primária com auto incremento
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # ID do episódio na API do Rick and Morty
    episode_id = Column(Integer, nullable=False)

    # Nome do episódio (armazenado para exibição sem precisar consultar a API)
    episode_name = Column(String, nullable=False)

    # Nota pessoal do usuário sobre o episódio
    nota = Column(String, nullable=True)

    # Avaliação de 1 a 5 estrelas
    avaliacao = Column(Integer, nullable=True)

    # Data e hora de criação da entrada
    created_at = Column(DateTime, default=datetime.utcnow)

    # Data e hora da última atualização
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

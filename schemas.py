# schemas.py
# Schemas Pydantic para validação de dados nas requisições e respostas da API

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class DiarioEntryCreate(BaseModel):
    """Schema para criar uma nova entrada no diário."""

    episode_id: int = Field(..., description="ID do episódio na API do Rick and Morty")
    episode_name: str = Field(..., description="Nome do episódio")
    nota: Optional[str] = Field(None, description="Nota pessoal sobre o episódio")
    avaliacao: Optional[int] = Field(None, ge=1, le=5, description="Avaliação de 1 a 5 estrelas")


class DiarioEntryUpdate(BaseModel):
    """Schema para atualizar uma entrada existente no diário (todos os campos são opcionais)."""

    nota: Optional[str] = Field(None, description="Nova nota pessoal")
    avaliacao: Optional[int] = Field(None, ge=1, le=5, description="Nova avaliação de 1 a 5")


class DiarioEntryOut(BaseModel):
    """Schema de saída — representa uma entrada completa com todos os campos, incluindo id e timestamps."""

    id: int
    episode_id: int
    episode_name: str
    nota: Optional[str]
    avaliacao: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        # Permite que o Pydantic leia dados diretamente de objetos ORM do SQLAlchemy
        from_attributes = True

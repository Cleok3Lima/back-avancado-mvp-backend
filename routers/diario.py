# routers/diario.py
# Rotas CRUD para o diário pessoal de episódios

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from database import get_db
from models import DiarioEntry
from schemas import DiarioEntryCreate, DiarioEntryUpdate, DiarioEntryOut

router = APIRouter(
    prefix="/diario",
    tags=["Diário"],
)


@router.get("/", response_model=List[DiarioEntryOut], summary="Listar entradas do diário")
def listar_entradas(
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(10, ge=1, le=100, description="Quantidade de itens por página"),
    avaliacao: Optional[int] = Query(None, ge=1, le=5, description="Filtrar por avaliação (1-5)"),
    order_by: Optional[str] = Query("created_at", description="Campo para ordenar: 'created_at' ou 'avaliacao'"),
    db: Session = Depends(get_db),
):
    """
    Retorna todas as entradas do diário com suporte a paginação, filtro por avaliação e ordenação.
    """
    query = db.query(DiarioEntry)

    # Filtro opcional por avaliação
    if avaliacao is not None:
        query = query.filter(DiarioEntry.avaliacao == avaliacao)

    # Ordenação
    if order_by == "avaliacao":
        query = query.order_by(desc(DiarioEntry.avaliacao))
    else:
        # Padrão: mais recentes primeiro
        query = query.order_by(desc(DiarioEntry.created_at))

    # Paginação: offset calcula quantos registros pular
    offset = (page - 1) * limit
    entradas = query.offset(offset).limit(limit).all()

    return entradas


@router.post("/", response_model=DiarioEntryOut, status_code=201, summary="Criar nova entrada no diário")
def criar_entrada(entrada: DiarioEntryCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova entrada no diário para um episódio específico.
    """
    nova_entrada = DiarioEntry(**entrada.model_dump())
    db.add(nova_entrada)
    db.commit()
    db.refresh(nova_entrada)
    return nova_entrada


@router.put("/{entry_id}", response_model=DiarioEntryOut, summary="Atualizar entrada do diário")
def atualizar_entrada(entry_id: int, dados: DiarioEntryUpdate, db: Session = Depends(get_db)):
    """
    Atualiza a nota e/ou avaliação de uma entrada existente no diário.
    Apenas os campos fornecidos serão atualizados.
    """
    entrada = db.query(DiarioEntry).filter(DiarioEntry.id == entry_id).first()

    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada não encontrada")

    # Atualiza apenas os campos que foram enviados (exclui os None)
    dados_atualizados = dados.model_dump(exclude_unset=True)
    for campo, valor in dados_atualizados.items():
        setattr(entrada, campo, valor)

    db.commit()
    db.refresh(entrada)
    return entrada


@router.delete("/{entry_id}", status_code=204, summary="Deletar entrada do diário")
def deletar_entrada(entry_id: int, db: Session = Depends(get_db)):
    """
    Remove permanentemente uma entrada do diário pelo seu ID.
    """
    entrada = db.query(DiarioEntry).filter(DiarioEntry.id == entry_id).first()

    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada não encontrada")

    db.delete(entrada)
    db.commit()

    # 204 No Content: sucesso sem corpo de resposta
    return None

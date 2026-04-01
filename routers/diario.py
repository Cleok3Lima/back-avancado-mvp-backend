# routers/diario.py
# Rotas CRUD para o diário pessoal de episódios — escopo por usuário autenticado

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from database import get_db
from models import DiarioEntry, User
from schemas import DiarioEntryCreate, DiarioEntryUpdate, DiarioEntryOut
from dependencies import get_current_user

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
    current_user: User = Depends(get_current_user),
):
    """
    Retorna as entradas do diário do usuário autenticado,
    com suporte a paginação, filtro por avaliação e ordenação.
    """
    query = db.query(DiarioEntry).filter(DiarioEntry.user_id == current_user.id)

    if avaliacao is not None:
        query = query.filter(DiarioEntry.avaliacao == avaliacao)

    if order_by == "avaliacao":
        query = query.order_by(desc(DiarioEntry.avaliacao))
    else:
        query = query.order_by(desc(DiarioEntry.created_at))

    offset = (page - 1) * limit
    entradas = query.offset(offset).limit(limit).all()

    return entradas


@router.post("/", response_model=DiarioEntryOut, status_code=201, summary="Criar nova entrada no diário")
def criar_entrada(
    entrada: DiarioEntryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Cria uma nova entrada no diário associada ao usuário autenticado.
    """
    nova_entrada = DiarioEntry(**entrada.model_dump(), user_id=current_user.id)
    db.add(nova_entrada)
    db.commit()
    db.refresh(nova_entrada)
    return nova_entrada


@router.put("/{entry_id}", response_model=DiarioEntryOut, summary="Atualizar entrada do diário")
def atualizar_entrada(
    entry_id: int,
    dados: DiarioEntryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Atualiza a nota e/ou avaliação de uma entrada do diário do usuário autenticado.
    Retorna 404 se a entrada não existir ou não pertencer ao usuário.
    """
    entrada = db.query(DiarioEntry).filter(
        DiarioEntry.id == entry_id,
        DiarioEntry.user_id == current_user.id,
    ).first()

    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada não encontrada")

    dados_atualizados = dados.model_dump(exclude_unset=True)
    for campo, valor in dados_atualizados.items():
        setattr(entrada, campo, valor)

    db.commit()
    db.refresh(entrada)
    return entrada


@router.delete("/{entry_id}", status_code=204, summary="Deletar entrada do diário")
def deletar_entrada(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Remove permanentemente uma entrada do diário do usuário autenticado.
    Retorna 404 se a entrada não existir ou não pertencer ao usuário.
    """
    entrada = db.query(DiarioEntry).filter(
        DiarioEntry.id == entry_id,
        DiarioEntry.user_id == current_user.id,
    ).first()

    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada não encontrada")

    db.delete(entrada)
    db.commit()
    return None

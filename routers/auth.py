# routers/auth.py
# Rotas de autenticação: cadastro, login e dados do usuário logado

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import UserCreate, UserOut, TokenOut, LoginRequest
from security import hash_password, verify_password, create_access_token
from dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/register", response_model=UserOut, status_code=201, summary="Cadastrar novo usuário")
def register(body: UserCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova conta de usuário.
    Retorna os dados do usuário criado (sem a senha).
    """
    if db.query(User).filter(User.username == body.username).first():
        raise HTTPException(status_code=400, detail="Nome de usuário já está em uso")

    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    novo_usuario = User(
        username=body.username,
        email=body.email,
        hashed_password=hash_password(body.password),
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


@router.post("/login", response_model=TokenOut, summary="Fazer login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    """
    Autentica o usuário com username e senha.
    Retorna um token JWT de acesso válido por 24 horas.
    """
    usuario = db.query(User).filter(User.username == body.username).first()

    if not usuario or not verify_password(body.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({"sub": str(usuario.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut, summary="Dados do usuário autenticado")
def me(current_user: User = Depends(get_current_user)):
    """
    Retorna os dados do usuário autenticado pelo token Bearer.
    """
    return current_user

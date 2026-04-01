# security.py
# Utilitários de criptografia: hash de senha, geração e decodificação de JWT

import os
from datetime import datetime, timedelta

import bcrypt
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

# Chave secreta para assinar os tokens JWT
# Em produção, defina a variável de ambiente SECRET_KEY com um valor aleatório seguro
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas

# Esquema OAuth2 — aponta para o endpoint de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(plain: str) -> str:
    """Retorna o hash bcrypt da senha em texto puro."""
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    """Verifica se a senha em texto puro corresponde ao hash armazenado."""
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(data: dict) -> str:
    """
    Gera um JWT assinado com os dados fornecidos e um prazo de expiração.
    O campo 'sub' deve conter o identificador do usuário (como string).
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """
    Decodifica e valida um JWT.
    Retorna o payload como dict, ou None se o token for inválido ou expirado.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

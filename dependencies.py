from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import User
from security import oauth2_scheme, decode_access_token


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Dependência que valida o Bearer token JWT e retorna o usuário autenticado.
    Deve ser injetada em qualquer endpoint protegido via Depends(get_current_user).
    Levanta HTTP 401 se o token for ausente, inválido ou expirado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user

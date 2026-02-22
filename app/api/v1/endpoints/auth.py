# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.crud import user as crud_user
from app.api.v1 import schemas

router = APIRouter()


@router.post("/register", response_model=schemas.UserOut, status_code=201)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para registrar un nuevo usuario.
    
    Valida que:
    - El correo tenga dominio @unal.edu.co
    - El correo no esté ya registrado
    - Los datos cumplan con los esquemas requeridos
    """
    # Verificar que el email no esté ya registrado
    db_user = crud_user.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )
    
    # Crear el usuario en la base de datos
    new_user = crud_user.create_user(db=db, user=user_in)
    
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el usuario"
        )
    
    return new_user

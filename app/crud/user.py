# app/crud/user.py
from sqlalchemy.orm import Session
from app.db import models
from app.api.v1 import schemas
from app.core.security import get_password_hash, verify_password


def get_user(db: Session, user_id: int):
    """Obtiene un usuario por su ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """Obtiene un usuario por su dirección de email."""
    return db.query(models.User).filter(models.User.email == email.lower()).first()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Crea un nuevo usuario en la base de datos.
    Hashea la contraseña antes de guardarla.
    """
    try:
        hashed_password = get_password_hash(user.password)
        db_user = models.User(
            name=user.name,
            email=user.email.lower(),
            hashed_password=hashed_password,
            role=user.role,
            phone_number=user.phone_number,
            gender=user.gender,
            major=user.major,
            age=user.age,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {e}")
        return None
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    """
    Autentica a un usuario.
    1. Busca al usuario por email.
    2. Si existe, verifica que la contraseña proporcionada coincida con la hasheada.
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_all_users(db: Session):
    """Retorna todos los usuarios en la base de datos."""
    return db.query(models.User).all()


def update_user(db: Session, user: models.User, user_update: schemas.UserUpdate):
    """
    Actualiza la información de un usuario existente.
    Solo actualiza los campos que fueron proporcionados (no None).
    """
    try:
        # Actualizar campos opcionales solo si fueron proporcionados
        if user_update.name is not None:
            user.name = user_update.name
        if user_update.phone_number is not None:
            user.phone_number = user_update.phone_number
        if user_update.gender is not None:
            user.gender = user_update.gender
        if user_update.major is not None:
            user.major = user_update.major
        if user_update.age is not None:
            user.age = user_update.age
        if user_update.role is not None:
            user.role = user_update.role
        if user_update.password is not None:
            user.hashed_password = get_password_hash(user_update.password)

        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        print(f"Error updating user: {e}")
        return None
    return user

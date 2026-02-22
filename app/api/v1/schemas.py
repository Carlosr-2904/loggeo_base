# app/api/v1/schemas.py
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Schema para crear un usuario"""
    name: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    major: Optional[str] = None
    age: Optional[int] = None
    role: Optional[str] = "estudiante"

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, v: str) -> str:
        """Valida que el email tenga dominio @unal.edu.co"""
        if not v.lower().endswith("@unal.edu.co"):
            raise ValueError("Solo se permiten correos con dominio @unal.edu.co")
        return v.lower()


class UserOut(BaseModel):
    """Schema para mostrar la información de un usuario (sin la contraseña)"""
    id: int
    created_at: datetime
    name: str
    email: EmailStr
    role: str
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    major: Optional[str] = None
    age: Optional[int] = None
    rating: Optional[float] = None

    class Config:
        from_attributes = True  # Permite que Pydantic lea datos desde modelos ORM


class Token(BaseModel):
    """Schema para el token JWT"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema para los datos del token"""
    email: Optional[EmailStr] = None

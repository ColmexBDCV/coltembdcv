from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user_auth_schema import UserAuthCreate
from schemas.user_info_schema import UserInfoCreate, UserInfoOut
from services.user_service import create_user, authenticate_user
from db.session import get_db

router = APIRouter()

# Registrar un nuevo usuario
@router.post("/register/", response_model=UserInfoOut, summary="Registrar usuario", description="Se registra un usuario para poder dar de alta nuevos sitios")
def register_user(auth_data: UserAuthCreate, info_data: UserInfoCreate, db: Session = Depends(get_db)):
    try:
        user_info = create_user(db, auth_data, info_data)
        return user_info
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Iniciar sesión (autenticación de usuario)
@router.post("/login/", summary="Logueo de usuario (En construccion)", description="Hay que implementar JWT para que funcione")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    token = authenticate_user(db, username, password)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Login successful", "token": token}

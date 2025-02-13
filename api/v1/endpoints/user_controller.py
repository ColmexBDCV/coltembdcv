from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from schemas.user_auth_schema import UserAuthCreate
from schemas.user_info_schema import UserInfoCreate, UserInfoOut
from services.user_service import create_user, authenticate_user, crear_token, existUser
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
def login_user(response: Response, username: str, password: str, db: Session = Depends(get_db)):
    user = existUser(db, username, password)
    print("USUARIO: ",user)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    else:
        token = crear_token({"usuario_id": user.user_auth_id})
        response.set_cookie(
            key="jwt",
            value=token,
            httponly=True,  # La cookie no es accesible desde JavaScript
            secure=True,     # Solo enviar en HTTPS
            max_age=7 * 24 * 60 * 60,  # Expira en 7 días
            samesite="strict"  # Protección contra CSRF
        )
    return {"user": user}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("jwt")  # Eliminar la cookie
    return {"message": "Sesión cerrada"}

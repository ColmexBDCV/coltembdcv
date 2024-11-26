from datetime import datetime, timedelta
import jwt

from sqlalchemy.orm import Session
from models.user_auth_model import UserAuth
from models.user_info_model import UserInfo
from schemas.user_auth_schema import UserAuthCreate
from schemas.user_info_schema import UserInfoCreate
from utils.security import hash_password, verify_password

KEY = '2c8878a8-b42e-4715-8b68-54669f510af9'
# Crear un nuevo usuario (autenticación y datos generales)
def create_user(db: Session, auth_data: UserAuthCreate, info_data: UserInfoCreate):
    hashed_password = hash_password(auth_data.password)

    # Crear la autenticación del usuario
    new_user_auth = UserAuth(username=auth_data.username, hashed_password=hashed_password)
    db.add(new_user_auth)
    db.commit()
    db.refresh(new_user_auth)

    # Crear la información general del usuario
    new_user_info = UserInfo(
        nombre=info_data.nombre,
        apellido_paterno=info_data.apellido_paterno,
        apellido_materno=info_data.apellido_materno,
        email=info_data.email,
        user_auth_id=new_user_auth.id
    )
    db.add(new_user_info)
    db.commit()
    db.refresh(new_user_info)

    return new_user_info

# Autenticar un usuario
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(UserAuth).filter(UserAuth.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    else:
        token = crear_token({"usuario_id": user.id})
    return token

# Generar un token
def crear_token(data: dict):
    datos_a_firmar = data.copy()
    datos_a_firmar["exp"] = datetime.utcnow() + timedelta(hours=1)  # Expira en 1 hora
    token = jwt.encode(datos_a_firmar, KEY, algorithm="HS256")
    return token

# Verificar un token
def verificar_token(token: str):
    try:
        payload = jwt.decode(token, KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # El token ha expirado
    except jwt.InvalidTokenError:
        return None  # El token no es válido
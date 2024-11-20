import bcrypt

# Función para generar un hash de la contraseña
def hash_password(password: str) -> str:
    # Genera un hash seguro usando bcrypt
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

# Función para verificar si la contraseña ingresada coincide con el hash almacenado
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Compara la contraseña en texto plano con el hash almacenado
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

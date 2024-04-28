# Importa Session para manejar sesiones de base de datos
from database import Session
# Importa la clase User para verificar las credenciales de los usuarios
from models import User


def verify_user(username, password):
    """Verifica las credenciales del usuario contra la base de datos.

    Args:
        username (str): Nombre de usuario ingresado.
        password (str): Contraseña ingresada.

    Returns:
        User: Objeto User si las credenciales son correctas, None de lo contrario.
    """
    session = Session()
    try:
        # Realiza la consulta en la base de datos para encontrar al usuario
        user = session.query(User).filter(User.username == username,
                                          User.password == password).first()
        return user
    finally:
        # Asegura que la sesión se cierre después de la consulta
        session.close()

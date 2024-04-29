# Importa Session para manejar sesiones de base de datos
from database import Session
# Importa la clase User para verificar las credenciales de los usuarios
from models import User


def verify_user(username, password, check_only=False):
    """Verifica las credenciales del usuario contra la base de datos.

    Args:
        username (str): Nombre de usuario ingresado.
        password (str): Contraseña ingresada.

    Returns:
        User: Objeto User si las credenciales son correctas, None de lo contrario.
    """
    session = Session()
    try:
        user = session.query(User).filter(User.username == username,
                                          User.password == password).first()
        if check_only:
            return user
        else:
            session.close()
            return user
    finally:
        if not check_only:
            session.close()

def update_tdp_status(user_id, status):
    """Actualiza el estado de aceptación de las políticas de tratamiento de datos personales."""
    session = Session()
    try:
        user = session.query(User).filter(User.id == user_id).one()
        user.tdp = status
        session.commit()
    finally:
        session.close()

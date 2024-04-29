# Importa Session para manejar sesiones de base de datos
from database import Session
# Importa el modelo User para interactuar con la tabla de usuarios
from models import User
# Importa exc para manejar excepciones específicas de SQLAlchemy
from sqlalchemy import exc
# Importa string para generar contraseñas seguras
import string
# Importa random para seleccionar caracteres aleatorios
import random


def generate_password(length=12):
    """Genera una contraseña segura de longitud especificada.

    Args:
        length (int): Longitud deseada para la contraseña. Por defecto es 12.

    Returns:
        str: La contraseña generada.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password


def username_exists(username):
    """Verifica si el nombre de usuario ya existe en la base de datos.

    Args:
        username (str): Nombre de usuario a verificar.

    Returns:
        bool: True si el nombre de usuario existe, False si no.
    """
    session = Session()
    user = session.query(User).filter(User.username == username).first()
    session.close()
    return user is not None


def create_user(username, password, role, full_name, phone_number):
    """Crea un nuevo usuario en la base de datos.

    Args:
        username (str): Nombre de usuario para el nuevo usuario.
        password (str): Contraseña para el nuevo usuario.
        role (str): Rol del nuevo usuario.
        full_name (str): Nombre completo del nuevo usuario.
        phone_number (str): Número de teléfono del nuevo usuario.

    Returns:
        str: Mensaje indicando si el usuario fue creado o no.
    """
    session = Session()
    try:
        if username_exists(username):
            return "El nombre de usuario ya existe."
        new_user = User(username=username, password=password, role=role,
                        full_name=full_name, phone_number=phone_number)
        session.add(new_user)
        session.commit()
        return "Usuario creado con éxito."
    except exc.IntegrityError:
        session.rollback()
        return "Error al crear el usuario."
    finally:
        session.close()


def search_users(search_query):
    """Busca usuarios que coincidan con un criterio de búsqueda en el nombre completo.

    Args:
        search_query (str): Criterio de búsqueda.

    Returns:
        list: Lista de objetos User que coinciden con la búsqueda.
    """
    session = Session()
    try:
        users = session.query(User).filter(User.full_name.ilike(f"%{search_query}%")).all()
        return users
    finally:
        session.close()


def update_user(user_id, new_username=None, new_password=None, new_role=None,
                new_full_name=None, new_phone_number=None):
    """Actualiza la información de un usuario existente.

    Args:
        user_id (int): ID del usuario a actualizar.
        new_username (str): Nuevo nombre de usuario (opcional).
        new_password (str): Nueva contraseña (opcional).
        new_role (str): Nuevo rol (opcional).
        new_full_name (str): Nuevo nombre completo (opcional).
        new_phone_number (str): Nuevo número de teléfono (opcional).

    Returns:
        str: Mensaje indicando si el usuario fue actualizado o no.
    """
    session = Session()
    try:
        user = session.query(User).filter(User.id == user_id).one_or_none()
        if user:
            user.username = new_username or user.username
            user.password = new_password or user.password
            user.role = new_role or user.role
            user.full_name = new_full_name or user.full_name
            user.phone_number = new_phone_number or user.phone_number
            session.commit()
            return "Usuario actualizado con éxito."
        else:
            return "Usuario no encontrado."
    finally:
        session.close()


def delete_user(user_id):
    """Elimina un usuario existente de la base de datos.

    Args:
        user_id (int): ID del usuario a eliminar.

    Returns:
        str: Mensaje indicando si el usuario fue eliminado o no.
    """
    session = Session()
    try:
        user = session.query(User).filter(User.id == user_id).one_or_none()
        if user:
            session.delete(user)
            session.commit()
            return "Usuario eliminado con éxito."
        else:
            return "Usuario no encontrado."
    finally:
        session.close()

def update_user_data(user):
    """Actualiza los datos de un usuario en la base de datos."""
    session = Session()
    try:
        session.add(user)  # SQLAlchemy maneja tanto nuevas instancias como instancias ya existentes
        session.commit()  # Realiza el commit de los cambios
    except Exception as e:
        session.rollback()  # Hace rollback en caso de error
        print(f"Error al actualizar los datos del usuario: {e}")
        raise e
    finally:
        session.close()

def update_user_terms(user_id, inicio, tdp):
    """Actualiza el estado de aceptación de términos y condiciones de un usuario."""
    session = Session()
    try:
        user = session.query(User).filter(User.id == user_id).one()
        user.inicio = inicio
        user.tdp = tdp
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error al actualizar los términos del usuario: {e}")  # Usar print o logging según tu configuración
        raise
    finally:
        session.close()

def handle_terms_acceptance(user):
    user.inicio = 1  # Marcar como que el usuario ha iniciado sesión al menos una vez
    user.tdp = "Aceptado"  # Registrar que ha aceptado los términos y condiciones
    update_user_data(user)  # Usar la función existente para guardar estos cambios

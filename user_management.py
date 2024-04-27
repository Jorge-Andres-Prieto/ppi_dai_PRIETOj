from database import Session
from models import User
from sqlalchemy import exc
import string
import random

def generate_password(length=12):
    """Genera una contraseña segura de longitud especificada."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def username_exists(username):
    """Verifica si el nombre de usuario ya existe en la base de datos."""
    session = Session()
    user = session.query(User).filter(User.username == username).first()
    session.close()
    return user is not None

def create_user(username, password, role, full_name, phone_number):
    session = Session()
    try:
        if username_exists(username):
            return "El nombre de usuario ya existe."
        new_user = User(username=username, password=password, role=role, full_name=full_name, phone_number=phone_number)
        session.add(new_user)
        session.commit()
        return "Usuario creado con éxito."
    except exc.IntegrityError:
        session.rollback()
        return "Error al crear el usuario."
    finally:
        session.close()

def search_users(search_query):
    session = Session()
    try:
        users = session.query(User).filter(User.full_name.ilike(f"%{search_query}%")).all()
        return users
    finally:
        session.close()

def update_user(user_id, new_username=None, new_password=None, new_role=None, new_full_name=None, new_phone_number=None):
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

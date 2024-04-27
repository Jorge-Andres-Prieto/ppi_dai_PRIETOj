from database import Session
from models import User
from sqlalchemy import exc

def create_user(username, password, role, full_name, phone_number):
    session = Session()
    try:
        new_user = User(username=username, password=password, role=role, full_name=full_name, phone_number=phone_number)
        session.add(new_user)
        session.commit()
        return "Usuario creado con éxito."
    except exc.IntegrityError:
        session.rollback()
        return "El nombre de usuario ya existe."
    finally:
        session.close()

def search_users(search_query):
    session = Session()
    try:
        users = session.query(User).filter(User.full_name.ilike(f"%{search_query}%")).all()
        return users
    finally:
        session.close()

def update_user(user_id, username=None, password=None, role=None, full_name=None, phone_number=None):
    session = Session()
    try:
        user = session.query(User).filter(User.id == user_id).one_or_none()
        if user:
            if username:
                user.username = username
            if password:
                user.password = password
            if role:
                user.role = role
            if full_name:
                user.full_name = full_name
            if phone_number:
                user.phone_number = phone_number
            session.commit()
            return "Usuario actualizado con éxito."
        else:
            return "Usuario no encontrado."
    finally:
        session.close()

def delete_user(user_id):
    session = Session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            session.delete(user)
            session.commit()
            return "Usuario eliminado con éxito."
        else:
            return "Usuario no encontrado."
    finally:
        session.close()

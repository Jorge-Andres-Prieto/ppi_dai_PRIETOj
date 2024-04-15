import os
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

# Utiliza la URL de la base de datos de las variables de entorno para mayor seguridad
DATABASE_URL = os.getenv("DATABASE_URL", "postgres://datos_usuarios_user:NNgnrDUS7HG3zQPuffAWnG3pyDvevRs2@dpg-coe966gl6cac73bvqv3g-a.oregon-postgres.render.com/datos_usuarios")
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def get_user(username):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user

def add_or_update_user(username, password, role):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if user:
        user.password = password
        user.role = role
    else:
        user = User(username=username, password=password, role=role)
        session.add(user)
    session.commit()
    session.close()

def delete_user(username):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if user:
        session.delete(user)
        session.commit()
    session.close()

def verify_login(username, password):
    """ Verifica las credenciales del usuario. """
    user = get_user(username)
    if user and user.password == password:
        return True, user.role
    return False, None

def app_admin():
    """ Interfaz de administrador para gestionar usuarios. """
    st.subheader("Administración de Usuarios")
    user_to_add = st.text_input("Usuario a añadir/modificar:")
    pass_to_add = st.text_input("Contraseña:", type="password")
    role_to_add = st.selectbox("Rol:", ['Admin', 'Empleado'])
    if st.button("Añadir/Modificar Usuario"):
        add_or_update_user(user_to_add, pass_to_add, role_to_add)
        st.success(f"Usuario {user_to_add} añadido/modificado como {role_to_add}")

    user_to_delete = st.selectbox("Eliminar Usuario:", [user.username for user in Session().query(User).all()])
    if st.button("Eliminar"):
        delete_user(user_to_delete)
        st.success(f"Usuario {user_to_delete} eliminado")

def app_empleado():
    """ Interfaz de empleado. """
    st.subheader("Bienvenido Empleado")

def main():
    st.title("Sistema de Login")

    # Gestionar sesión de usuario
    if 'username' not in st.session_state or 'role' not in st.session_state:
        username = st.sidebar.text_input("Usuario")
        password = st.sidebar.text_input("Contraseña", type="password")
        if st.sidebar.button("Login"):
            authenticated, role = verify_login(username, password)
            if authenticated:
                st.session_state['username'] = username
                st.session_state['role'] = role
                st.sidebar.success("Login exitoso")
            else:
                st.sidebar.error("Usuario o contraseña incorrectos")

    if 'username' in st.session_state and 'role' in st.session_state:
        if st.session_state['role'] == 'Admin':
            app_admin()
        elif st.session_state['role'] == 'Empleado':
            app_empleado()
        if st.sidebar.button("Logout"):
            del st.session_state['username']
            del st.session_state['role']

if __name__ == "__main__":
    main()

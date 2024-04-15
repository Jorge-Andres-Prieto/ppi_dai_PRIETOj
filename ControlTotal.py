import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definición del modelo de base de datos
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

# Conexión a la base de datos PostgreSQL
DATABASE_URL = "postgresql://datos_usuarios_user:NNgnrDUS7HG3zQPuffAWnG3pyDvevRs2@dpg-coe966gl6cac73bvqv3g-a.oregon-postgres.render.com/datos_usuarios"
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def create_user(username, password, role, full_name, phone_number):
    session = Session()
    try:
        new_user = User(username=username, password=password, role=role, full_name=full_name, phone_number=phone_number)
        session.add(new_user)
        session.commit()
        return f"Usuario {username} creado con éxito."
    except exc.IntegrityError:
        session.rollback()
        return "Error: el nombre de usuario ya existe."
    finally:
        session.close()

def read_user_by_username(username):
    session = Session()
    try:
        user = session.query(User).filter(User.username == username).first()
        return user
    finally:
        session.close()

def update_user(username, new_password, new_role, new_full_name, new_phone_number):
    session = Session()
    user = read_user_by_username(username)
    if user:
        user.password = new_password if new_password else user.password
        user.role = new_role if new_role else user.role
        user.full_name = new_full_name if new_full_name else user.full_name
        user.phone_number = new_phone_number if new_phone_number else user.phone_number
        session.commit()
        return f"Usuario '{username}' actualizado con éxito."
    return "Usuario no encontrado."

def delete_user(id):
    session = Session()
    try:
        user = session.query(User).filter(User.id == id).first()
        if user:
            session.delete(user)
            session.commit()
            return f"Usuario {id} eliminado con éxito."
        return "Usuario no encontrado."
    finally:
        session.close()

st.title("Sistema de Gestión de Usuarios")

option = st.sidebar.selectbox(
    '¿Qué deseas hacer?',
    ('Crear Usuario', 'Buscar Usuario', 'Actualizar Usuario', 'Eliminar Usuario')
)

if option == 'Crear Usuario':
    with st.container():
        username = st.text_input("Nombre de Usuario")
        password = st.text_input("Contraseña", type="password")
        role = st.selectbox("Rol", ["Admin", "Empleado"])
        full_name = st.text_input("Nombre Completo")
        phone_number = st.text_input("Número de Celular")
        if st.button("Crear"):
            result = create_user(username, password, role, full_name, phone_number)
            st.success(result)

elif option == 'Buscar Usuario':
    with st.container():
        username = st.text_input("Nombre de Usuario a buscar")
        if st.button("Buscar"):
            user = read_user_by_username(username)
            if user:
                st.write(f"ID: {user.id}, Nombre de Usuario: {user.username}, Rol: {user.role}, Nombre Completo: {user.full_name}, Teléfono: {user.phone_number}")
            else:
                st.write("Usuario no encontrado")

elif option == 'Actualizar Usuario':
    with st.container():
        username = st.text_input("Nombre de Usuario a actualizar")
        if st.button("Buscar Usuario"):
            user = read_user_by_username(username)
            if user:
                new_password = st.text_input("Nueva Contraseña", type="password")
                new_role = st.text_input("Nuevo Rol")
                new_full_name = st.text_input("Nuevo Nombre Completo")
                new_phone_number = st.text_input("Nuevo Número de Celular")
                if st.button("Actualizar Usuario"):
                    result = update_user(username, new_password, new_role, new_full_name, new_phone_number)
                    st.success(result)
            else:
                st.error("Usuario no encontrado")

elif option == 'Eliminar Usuario':
    with st.container():
        id = st.number_input("ID del Usuario a eliminar", step=1)
        if st.button("Eliminar"):
            result = delete_user(id)
            st.success(result)

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

# Conexión a la base de datos PostgreSQL
DATABASE_URL = st.secrets["DATABASE_URL"]
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

# Funciones CRUD
def create_user(username, password, role):
    session = Session()
    try:
        new_user = User(username=username, password=password, role=role)
        session.add(new_user)
        session.commit()
        return f"Usuario {username} creado con éxito."
    except exc.IntegrityError:
        return "Error: el nombre de usuario ya existe."
    finally:
        session.close()

def read_users():
    session = Session()
    try:
        users = session.query(User).all()
        return users
    finally:
        session.close()

def update_user(id, new_username, new_password, new_role):
    session = Session()
    try:
        user = session.query(User).filter(User.id == id).first()
        if user:
            user.username = new_username
            user.password = new_password
            user.role = new_role
            session.commit()
            return f"Usuario {id} actualizado con éxito."
        return "Usuario no encontrado."
    finally:
        session.close()

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

# Interfaz de Streamlit
st.title("Sistema de Gestión de Usuarios")

if st.checkbox("Crear Usuario"):
    username = st.text_input("Nombre de Usuario", key="create_username")
    password = st.text_input("Contraseña", type="password", key="create_password")
    role = st.selectbox("Rol", ["Admin", "Empleado"], key="create_role")
    if st.button("Crear"):
        result = create_user(username, password, role)
        st.success(result)

if st.checkbox("Mostrar Usuarios"):
    users = read_users()
    for user in users:
        st.text(f"ID: {user.id}, Nombre: {user.username}, Rol: {user.role}")

if st.checkbox("Actualizar Usuario"):
    id = st.number_input("ID del Usuario a actualizar", step=1, key="update_id")
    new_username = st.text_input("Nuevo Nombre de Usuario", key="update_username")
    new_password = st.text_input("Nueva Contraseña", type="password", key="update_password")
    new_role = st.selectbox("Nuevo Rol", ["Admin", "Empleado"], key="update_role")
    if st.button("Actualizar"):
        result = update_user(id, new_username, new_password, new_role)
        st.success(result)

if st.checkbox("Eliminar Usuario"):
    del_id = st.number_input("ID del Usuario a eliminar", step=1, key="delete_id")
    if st.button("Eliminar"):
        result = delete_user(del_id)
        st.success(result)

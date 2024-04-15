import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

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
session_factory = sessionmaker(bind=engine)

# Crear las tablas si no existen
Base.metadata.create_all(engine)

def authenticate_user(username, password):
    session = session_factory()
    try:
        user = session.query(User).filter(User.username == username, User.password == password).one_or_none()
        return user
    finally:
        session.close()

# App de Streamlit
def main():
    st.title("Control Total")
    username = st.sidebar.text_input("Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Iniciar sesión"):
        user = authenticate_user(username, password)
        if user:
            if user.role == "Admin":
                app_admin(user)
            else:
                st.success("Bienvenido a WELCOME")
        else:
            st.error("Usuario o contraseña incorrectos")

def app_admin(user):
    st.title("Gestión de Usuarios")
    option = st.sidebar.selectbox(
        '¿Qué deseas hacer?',
        ('Crear Usuario', 'Buscar Usuario', 'Actualizar Usuario', 'Eliminar Usuario')
    )

    if option == 'Crear Usuario':
        create_user_form()
    elif option == 'Buscar Usuario':
        search_user()
    elif option == 'Actualizar Usuario':
        update_user_form()
    elif option == 'Eliminar Usuario':
        delete_user_form()

def create_user_form():
    with st.container():
        username = st.text_input("Nombre de Usuario")
        password = st.text_input("Contraseña", type="password")
        role = st.selectbox("Rol", ["Admin", "Empleado"])
        full_name = st.text_input("Nombre Completo")
        phone_number = st.text_input("Número de Celular")
        if st.button("Crear"):
            result = create_user(username, password, role, full_name, phone_number)
            st.success(result)

def search_user():
    with st.container():
        search_name = st.text_input("Nombre a buscar")
        if st.button("Buscar"):
            users = read_user_by_name(search_name)
            if users:
                for user in users:
                    st.write(f"ID: {user.id}, Nombre: {user.full_name}, Usuario: {user.username}, Rol: {user.role}, Teléfono: {user.phone_number}")
            else:
                st.write("No se encontraron usuarios")

def update_user_form():
    with st.container():
        update_id = st.number_input("ID del Usuario a actualizar", step=1)
        new_username = st.text_input("Nuevo Nombre de Usuario", placeholder="Dejar en blanco si no desea cambiar")
        new_password = st.text_input("Nueva Contraseña", type="password", placeholder="Dejar en blanco si no desea cambiar")
        new_role = st.selectbox("Nuevo Rol", ["", "Admin", "Empleado"], index=0, format_func=lambda x: x if x else "Dejar en blanco")
        new_full_name = st.text_input("Nuevo Nombre Completo", placeholder="Dejar en blanco si no desea cambiar")
        new_phone_number = st.text_input("Nuevo Número de Celular", placeholder="Dejar en blanco si no desea cambiar")
        if st.button("Actualizar"):
            result = update_user(update_id, new_username or None, new_password or None, new_role if new_role else None, new_full_name or None, new_phone_number or None)
            st.success(result)

def delete_user_form():
    with st.container():
        del_id = st.number_input("ID del Usuario a eliminar", step=1)
        if st.button("Eliminar"):
            result = delete_user(del_id)
            st.success(result)

if __name__ == "__main__":
    main()

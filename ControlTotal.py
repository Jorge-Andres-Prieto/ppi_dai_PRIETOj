import streamlit as st
import pandas as pd
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

# Crear las tablas si no existen
Base.metadata.create_all(engine)

def authenticate_user(username, password):
    session = Session()
    try:
        query = session.query(User.username, User.password, User.role).all()
        df_users = pd.DataFrame(query, columns=['username', 'password', 'role'])
        user_row = df_users[(df_users['username'] == username) & (df_users['password'] == password)]
        if not user_row.empty:
            return user_row.iloc[0].to_dict()
        return None
    finally:
        session.close()

# Iniciar sesión y almacenar el estado en session_state
def login():
    user = authenticate_user(st.session_state.username, st.session_state.password)
    if user:
        st.session_state['authenticated'] = True
        st.session_state['role'] = user['role']
        st.session_state['username'] = user['username']
        st.experimental_rerun()
    else:
        st.error("Usuario o contraseña incorrectos")
        st.session_state['authenticated'] = False

# Verificar si se ha autenticado previamente, para mantener sesión activa
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['role'] = None
    st.session_state['username'] = None

# Pantalla de Login
if not st.session_state['authenticated']:
    st.title("Control Total")
    st.session_state.username = st.text_input("Usuario")
    st.session_state.password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar", on_click=login):
        st.stop()

# Pantallas de Usuario
if st.session_state['authenticated']:
    if st.session_state['role'] == 'Admin':
        st.title("Gestión de Usuarios")

        option = st.sidebar.selectbox(
            '¿Qué deseas hacer?',
            ('Crear Usuario', 'Buscar Usuario', 'Actualizar Usuario', 'Eliminar Usuario')
        )

        if option == 'Crear Usuario':
            username = st.text_input("Nombre de Usuario")
            password = st.text_input("Contraseña", type="password")
            role = st.selectbox("Rol", ["Admin", "Empleado"])
            full_name = st.text_input("Nombre Completo")
            phone_number = st.text_input("Número de Celular")
            if st.button("Crear"):
                session = Session()
                try:
                    new_user = User(username=username, password=password, role=role, full_name=full_name, phone_number=phone_number)
                    session.add(new_user)
                    session.commit()
                    st.success(f"Usuario {username} creado con éxito.")
                except exc.IntegrityError:
                    session.rollback()
                    st.error("Error: el nombre de usuario ya existe.")
                finally:
                    session.close()

        elif option == 'Buscar Usuario':
            search_name = st.text_input("Nombre a buscar")
            if st.button("Buscar"):
                session = Session()
                try:
                    users = session.query(User).filter(User.full_name.ilike(f"%{search_name}%")).all()
                    if users:
                        for user in users:
                            st.write(f"ID: {user.id}, Nombre: {user.full_name}, Usuario: {user.username}, Rol: {user.role}, Teléfono: {user.phone_number}")
                    else:
                        st.write("No se encontraron usuarios")
                finally:
                    session.close()

        elif option == 'Actualizar Usuario':
            update_id = st.number_input("ID del Usuario a actualizar", step=1)
            new_username = st.text_input("Nuevo Nombre de Usuario")
            new_password = st.text_input("Nueva Contraseña", type="password")
            new_role = st.selectbox("Nuevo Rol", ["Admin", "Empleado"])
            new_full_name = st.text_input("Nuevo Nombre Completo")
            new_phone_number = st.text_input("Nuevo Número de Celular")
            if st.button("Actualizar"):
                session = Session()
                try:
                    user = session.query(User).filter(User.id == update_id).one_or_none()
                    if user:
                        user.username = new_username
                        user.password = new_password
                        user.role = new_role
                        user.full_name = new_full_name
                        user.phone_number = new_phone_number
                        session.commit()
                        st.success(f"Usuario {update_id} actualizado con éxito.")
                    else:
                        st.error("Usuario no encontrado.")
                finally:
                    session.close()

        elif option == 'Eliminar Usuario':
            del_id = st.number_input("ID del Usuario a eliminar", step=1)
            if st.button("Eliminar"):
                session = Session()
                try:
                    user = session.query(User).filter(User.id == del_id).one_or_none()
                    if user:
                        session.delete(user)
                        session.commit()
                        st.success(f"Usuario {del_id} eliminado con éxito.")
                    else:
                        st.error("Usuario no encontrado.")
                finally:
                    session.close()

    elif st.session_state['role'] == 'Empleado':
        st.title("WELCOME")

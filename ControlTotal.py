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

# Crear las tablas si no existen
Base.metadata.create_all(engine)

# Funciones de gestión de usuarios
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

def user_login(username, password):
    session = Session()
    try:
        user = session.query(User).filter(User.username == username, User.password == password).first()
        return user
    finally:
        session.close()

# App de Streamlit
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        manage_users()
    else:
        login()

def login():
    st.title("Control Total")
    
    username = st.text_input("Nombre de usuario")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar sesión"):
        user = user_login(username, password)
        if user:
            st.session_state['logged_in'] = True
            st.session_state['role'] = user.role
            st.experimental_rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

def manage_users():
    st.title("Gestión de Usuarios")
    
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
            search_name = st.text_input("Nombre a buscar")
            if st.button("Buscar"):
                users = read_user_by_name(search_name)
                if users:
                    for user in users:
                        st.write(f"ID: {user.id}, Nombre: {user.full_name}, Usuario: {user.username}, Rol: {user.role}, Teléfono: {user.phone_number}")
                else:
                    st.write("No se encontraron usuarios")

    elif option == 'Actualizar Usuario':
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

    elif option == 'Eliminar Usuario':
        with st.container():
            del_id = st.number_input("ID del Usuario a eliminar", step=1)
            if st.button("Eliminar"):
                result = delete_user(del_id)
                st.success(result)

if __name__ == "__main__":
    main()

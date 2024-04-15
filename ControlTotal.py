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

def verify_user(username, password):
    session = Session()
    try:
        user = session.query(User).filter(User.username == username, User.password == password).first()
        return user
    finally:
        session.close()

# Interfaz de Login
def main():
    st.title("Control Total")
    username = st.text_input("Nombre de Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        user = verify_user(username, password)
        if user:
            st.session_state['user'] = user
            st.experimental_rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")

if 'user' not in st.session_state:
    main()
else:
    user = st.session_state['user']
    if user.role == "Admin":
        st.title("Sistema de Gestión de Usuarios")
        option = st.sidebar.selectbox(
            '¿Qué deseas hacer?',
            ('Crear Usuario', 'Buscar Usuario', 'Actualizar Usuario', 'Eliminar Usuario')
        )

        if option == 'Crear Usuario':
            with st.form("Crear Usuario"):
                username = st.text_input("Nombre de Usuario")
                password = st.text_input("Contraseña", type="password")
                role = st.selectbox("Rol", ["Admin", "Empleado"])
                full_name = st.text_input("Nombre Completo")
                phone_number = st.text_input("Número de Celular")
                submitted = st.form_submit_button("Crear")
                if submitted:
                    session = Session()
                    try:
                        new_user = User(username=username, password=password, role=role, full_name=full_name, phone_number=phone_number)
                        session.add(new_user)
                        session.commit()
                        st.success(f"Usuario {username} creado con éxito.")
                    except exc.IntegrityError:
                        session.rollback()
                        st.error("El nombre de usuario ya existe.")
                    finally:
                        session.close()

        elif option == 'Buscar Usuario':
            search_name = st.text_input("Nombre a buscar")
            if st.button("Buscar"):
                session = Session()
                users = session.query(User).filter(User.full_name.ilike(f"%{search_name}%")).all()
                session.close()
                if users:
                    for user in users:
                        st.write(f"ID: {user.id}, Nombre: {user.full_name}, Usuario: {user.username}, Rol: {user.role}, Teléfono: {user.phone_number}")
                else:
                    st.write("No se encontraron usuarios")

        elif option == 'Actualizar Usuario':
            update_id = st.number_input("ID del Usuario a actualizar", step=1)
            new_username = st.text_input("Nuevo Nombre de Usuario", placeholder="Dejar en blanco si no desea cambiar")
            new_password = st.text_input("Nueva Contraseña", type="password", placeholder="Dejar en blanco si no desea cambiar")
            new_role = st.selectbox("Nuevo Rol", ["", "Admin", "Empleado"], index=0, format_func=lambda x: x if x else "Dejar en blanco")
            new_full_name = st.text_input("Nuevo Nombre Completo", placeholder="Dejar en blanco si no desea cambiar")
            new_phone_number = st.text_input("Nuevo Número de Celular", placeholder="Dejar en blanco si no desea cambiar")
            if st.button("Actualizar"):
                session = Session()
                user = session.query(User).filter(User.id == update_id).one_or_none()
                if user:
                    user.username = new_username or user.username
                    user.password = new_password or user.password
                    user.role = new_role or user.role
                    user.full_name = new_full_name or user.full_name
                    user.phone_number = new_phone_number or user.phone_number
                    session.commit()
                    session.close()
                    st.success(f"Usuario {update_id} actualizado con éxito.")
                else:
                    st.error("Usuario no encontrado.")

        elif option == 'Eliminar Usuario':
            del_id = st.number_input("ID del Usuario a eliminar", step=1)
            if st.button("Eliminar"):
                session = Session()
                user = session.query(User).filter(User.id == del_id).first()
                if user:
                    session.delete(user)
                    session.commit()
                    session.close()
                    st.success(f"Usuario {del_id} eliminado con éxito.")
                else:
                    st.error("Usuario no encontrado.")

    elif user.role == "Empleado":
        st.title("WELCOME")

    if st.button("Cerrar Sesión"):
        del st.session_state['user']
        st.experimental_rerun()

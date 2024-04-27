import streamlit as st
from auth import verify_user
from user_management import create_user, search_users, update_user, delete_user

def main():
    st.title("Control Total")
    if 'user' not in st.session_state:
        username = st.text_input("Nombre de Usuario")
        password = st.text_input("Contraseña", type="password")
        if st.button("Ingresar"):
            user = verify_user(username, password)
            if user:
                st.session_state['user'] = user
                st.experimental_rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")
    else:
        user = st.session_state['user']
        if user.role == "Admin":
            st.title("Sistema de Gestión de Usuarios")
            option = st.sidebar.selectbox(
                '¿Qué deseas hacer?',
                ('Crear Usuario', 'Buscar Usuario', 'Actualizar Usuario', 'Eliminar Usuario')
            )
            if option == 'Crear Usuario':
                create_user_form()
            elif option == 'Buscar Usuario':
                search_user_form()
            elif option == 'Actualizar Usuario':
                update_user_form()
            elif option == 'Eliminar Usuario':
                delete_user_form()
        elif user.role == "Empleado":
            st.title("Bienvenido Empleado")
        if st.button("Cerrar Sesión"):
            del st.session_state['user']
            st.experimental_rerun()

def create_user_form():
    with st.form("Crear Usuario"):
        username = st.text_input("Nombre de Usuario")
        password = st.text_input("Contraseña", type="password")
        role = st.selectbox("Rol", ["Admin", "Empleado"])
        full_name = st.text_input("Nombre Completo")
        phone_number = st.text_input("Número de Celular")
        submitted = st.form_submit_button("Crear")
        if submitted:
            result = create_user(username, password, role, full_name, phone_number)
            if "éxito" in result:
                st.success(result)
            else:
                st.error(result)

def search_user_form():
    search_name = st.text_input("Nombre a buscar")
    if st.button("Buscar"):
        users = search_users(search_name)
        if users:
            for user in users:
                st.write(f"ID: {user.id}, Nombre: {user.full_name}, Usuario: {user.username}, Rol: {user.role}, Teléfono: {user.phone_number}")
        else:
            st.write("No se encontraron usuarios")

def update_user_form():
    update_id = st.number_input("ID del Usuario a actualizar", step=1)
    new_username = st.text_input("Nuevo Nombre de Usuario", placeholder="Dejar en blanco si no desea cambiar")
    new_password = st.text_input("Nueva Contraseña", type="password", placeholder="Dejar en blanco si no desea cambiar")
    new_role = st.selectbox("Nuevo Rol", ["", "Admin", "Empleado"], index=0, format_func=lambda x: x if x else "Dejar en blanco")
    new_full_name = st.text_input("Nuevo Nombre Completo", placeholder="Dejar en blanco si no desea cambiar")
    new_phone_number = st.text_input("Nuevo Número de Celular", placeholder="Dejar en blanco si no desea cambiar")
    if st.button("Actualizar"):
        result = update_user(update_id, new_username, new_password, new_role, new_full_name, new_phone_number)
        if "éxito" in result:
            st.success(result)
        else:
            st.error(result)

def delete_user_form():
    del_id = st.number_input("ID del Usuario a eliminar", step=1)
    if st.button("Eliminar"):
        result = delete_user(del_id)
        if "éxito" in result:
            st.success(result)
        else:
            st.error(result)

if __name__ == "__main__":
    main()

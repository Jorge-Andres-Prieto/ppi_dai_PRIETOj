import streamlit as st
from streamlit_option_menu import option_menu
from auth import verify_user
from user_management import create_user, search_users, update_user, delete_user, generate_password

st.set_page_config(page_title="Control Total", layout="wide")

def main():
    if 'user' not in st.session_state:
        st.title("Control Total")
        login_form()
    else:
        user = st.session_state['user']
        main_menu(user)

def login_form():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("Nombre de Usuario")
        password = st.text_input("Contraseña", type="password")
        if st.button("Ingresar"):
            user = verify_user(username, password)
            if user:
                st.session_state['user'] = user
                st.experimental_rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")

def main_menu(user):
    with st.sidebar:
        selected = option_menu(
            None,
            ["Admin", "Ventas y Facturación", "Gestión de inventarios", "Análisis estadísticos", "Domicilios"],
            icons=["person-circle", "currency-dollar", "archive", "graph-up", "truck"],
            menu_icon="cast",
            default_index=0
        )
        if st.button("Cerrar Sesión"):
            logout()

    if selected == 'Admin' and user.role == "Admin":
        admin_menu()

def logout():
    if 'user' in st.session_state:
        del st.session_state['user']
    st.experimental_rerun()

def admin_menu():
    selected = option_menu(
        None,
        ["Crear Usuario", "Buscar Usuario", "Actualizar Usuario", "Eliminar Usuario"],
        icons=["plus-circle", "search", "pencil-square", "trash"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )
    if selected == 'Crear Usuario':
        create_user_form()
    elif selected == 'Buscar Usuario':
        search_user_form()
    elif selected == 'Actualizar Usuario':
        update_user_form()
    elif selected == 'Eliminar Usuario':
        delete_user_form()

def create_user_form():
    with st.form("Crear Usuario"):
        username = st.text_input("Nombre de Usuario", help="Debe ser único.")
        auto_password = st.checkbox("Generar contraseña segura automáticamente")
        password = generate_password() if auto_password else st.text_input("Contraseña", type="password")
        role = st.selectbox("Rol", ["Admin", "Empleado"])
        full_name = st.text_input("Nombre Completo")
        phone_number = st.text_input("Número de Celular", help="Formato válido: +1234567890")
        submitted = st.form_submit_button("Crear")
        if submitted:
            validate_and_submit_user(username, password, role, full_name, phone_number, auto_password)

def validate_and_submit_user(username, password, role, full_name, phone_number, auto_password):
    if len(username) < 5:
        st.error("El nombre de usuario debe tener al menos 5 caracteres.")
    elif not auto_password and len(password) < 8:
        st.error("La contraseña debe tener al menos 8 caracteres.")
    else:
        result = create_user(username, password, role, full_name, phone_number)
        if "éxito" in result:
            st.success(result)
            if auto_password:
                st.info(f"Contraseña generada automáticamente: {password}")
        else:
            st.error(result)

def search_user_form():
    with st.form("Buscar Usuario"):
        search_name = st.text_input("Nombre a buscar")
        submitted = st.form_submit_button("Buscar")
        if submitted:
            display_search_results(search_name)

def display_search_results(search_name):
    users = search_users(search_name)
    if users:
        for user in users:
            st.write(f"ID: {user.id}, Nombre: {user.full_name}, Usuario: {user.username}, Rol: {user.role}, Teléfono: {user.phone_number}")
    else:
        st.write("No se encontraron usuarios")

def update_user_form():
    with st.form("Actualizar Usuario"):
        update_id = st.number_input("ID del Usuario a actualizar", step=1)
        new_username = st.text_input("Nuevo Nombre de Usuario", placeholder="Dejar en blanco si no desea cambiar")
        new_password = st.text_input("Nueva Contraseña", type="password", placeholder="Dejar en blanco si no desea cambiar")
        new_role = st.selectbox("Nuevo Rol", ["", "Admin", "Empleado"], index=0, format_func=lambda x: x if x else "Dejar en blanco")
        new_full_name = st.text_input("Nuevo Nombre Completo", placeholder="Dejar en blanco si no desea cambiar")
        new_phone_number = st.text_input("Nuevo Número de Celular", placeholder="Dejar en blanco si no desea cambiar")
        submitted = st.form_submit_button("Actualizar")
        if submitted:
            result = update_user(update_id, new_username, new_password, new_role, new_full_name, new_phone_number)
            if "éxito" in result:
                st.success(result)
            else:
                st.error(result)

def delete_user_form():
    with st.form("Eliminar Usuario"):
        del_id = st.number_input("ID del Usuario a eliminar", step=1)
        submitted = st.form_submit_button("Eliminar")
        if submitted:
            result = delete_user(del_id)
            if "éxito" in result:
                st.success(result)
            else:
                st.error(result)

if __name__ == "__main__":
    main()

# Importa el módulo de Streamlit para crear aplicaciones web
import streamlit as st
# Importa opciones de menú para la navegación en la aplicación
from streamlit_option_menu import option_menu
# Importa la función para verificar la autenticidad del usuario
from auth import verify_user
# Importa funciones para manejar la creación, búsqueda, actualización y eliminación de usuarios
from user_management import create_user, search_users, update_user, delete_user, generate_password


st.set_page_config(page_title="Control Total", layout="wide")


def main():
    """Función principal que controla el flujo de la aplicación.

    Args:
        None

    Returns:
        None
    """
    if 'user' not in st.session_state:
        login_page()
    else:
        user = st.session_state['user']
        main_menu(user)


def login_page():
    """Crea y gestiona la página de inicio de sesión.

    Args:
        None

    Returns:
        None
    """
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
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


def main_menu(user):
    """Crea y muestra el menú principal para la navegación de la aplicación.

    Args:
        user (dict): Diccionario que contiene la información del usuario autenticado.

    Returns:
        None
    """
    with st.sidebar:
        selected = option_menu(
            None,
            ["Admin", "Ventas y Facturación", "Gestión de inventarios",
             "Análisis estadísticos", "Domicilios"],
            icons=["person-circle", "currency-dollar", "archive", "graph-up",
                   "truck"],
            menu_icon="cast",
            default_index=0
        )
        if st.button("Cerrar Sesión"):
            logout()

    if selected == 'Admin' and user.role == "Admin":
        admin_menu()


def logout():
    """Cierra la sesión del usuario y reinicia la aplicación.

    Args:
        None

    Returns:
        None
    """
    if 'user' in st.session_state:
        del st.session_state['user']
    st.experimental_rerun()


def admin_menu():
    """Muestra el menú de administración para la gestión de usuarios.

    Args:
        None

    Returns:
        None
    """
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
    """Formulario para crear un nuevo usuario.

    Args:
        None

    Returns:
        None
    """
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
    """Valida la información del usuario y, si es válida, crea un nuevo usuario.

    Args:
        username (str): Nombre de usuario a crear.
        password (str): Contraseña para el usuario.
        role (str): Rol del usuario en la aplicación.
        full_name (str): Nombre completo del usuario.
        phone_number (str): Número de teléfono del usuario.
        auto_password (bool): Indica si la contraseña fue generada automáticamente.

    Returns:
        None
    """
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
    """Formulario para buscar usuarios existentes en la base de datos.

    Args:
        None

    Returns:
        None
    """
    with st.form("Buscar Usuario"):
        search_name = st.text_input("Nombre a buscar")
        submitted = st.form_submit_button("Buscar")
        if submitted:
            display_search_results(search_name)


def display_search_results(search_name):
    """Muestra los resultados de la búsqueda de usuarios.

    Args:
        search_name (str): Nombre del usuario a buscar.

    Returns:
        None
    """
    users = search_users(search_name)
    if users:
        for user in users:
            st.write(
                f"ID: {user.id}, Nombre: {user.full_name}, Usuario: {user.username}, Rol: {user.role}, Teléfono: {user.phone_number}")
    else:
        st.write("No se encontraron usuarios")


def update_user_form():
    """Formulario para actualizar la información de un usuario existente con opciones seleccionables.

    Args:
        None

    Returns:
        None
    """
    st.write("Actualizar Usuario")
    update_id = st.number_input("ID del Usuario a actualizar", step=1)

    # Opciones para seleccionar qué campos actualizar
    update_username = st.checkbox("Actualizar nombre de usuario")
    update_password = st.checkbox("Actualizar contraseña")
    update_role = st.checkbox("Actualizar rol")
    update_full_name = st.checkbox("Actualizar nombre completo")
    update_phone_number = st.checkbox("Actualizar número de teléfono")

    # Botón para mostrar los campos de entrada según las selecciones
    modify = st.button("Modificar")

    # Diccionario para almacenar los nuevos valores
    new_values = {}

    if modify:
        if update_username:
            new_values['new_username'] = st.text_input("Nuevo Nombre de Usuario")
        if update_password:
            new_values['new_password'] = st.text_input("Nueva Contraseña", type="password")
        if update_role:
            new_values['new_role'] = st.selectbox("Nuevo Rol", ["", "Admin", "Empleado"], index=0)
        if update_full_name:
            new_values['new_full_name'] = st.text_input("Nuevo Nombre Completo")
        if update_phone_number:
            new_values['new_phone_number'] = st.text_input("Nuevo Número de Celular")

        # Botón para actualizar la información en la base de datos
        update = st.button("Actualizar")

        if update:
            # Llamada a la función de actualización con los valores recogidos
            result = update_user(
                update_id,
                new_username=new_values.get('new_username'),
                new_password=new_values.get('new_password'),
                new_role=new_values.get('new_role'),
                new_full_name=new_values.get('new_full_name'),
                new_phone_number=new_values.get('new_phone_number')
            )
            if "éxito" in result:
                st.success(result)
            else:
                st.error(result)

def delete_user_form():
    """Formulario para eliminar un usuario existente.

    Args:
        None

    Returns:
        None
    """
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

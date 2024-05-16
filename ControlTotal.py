# Importa el módulo de Streamlit para crear aplicaciones web
import streamlit as st

# Importa opciones de menú para la navegación en la aplicación
from streamlit_option_menu import option_menu

# Importa la función para verificar la autenticidad del usuario
from auth import verify_user, update_tdp_status

# Importa funciones para manejar la creación, búsqueda, actualización y eliminación de usuarios
from user_management import create_user, search_users, update_user, delete_user, generate_password

# Importa funciones para la gestión de productos
from product_management import search_products, delete_product, update_product, add_product

from client_management import create_client, search_clients, update_client, delete_client


# Importa funcion para crear la base de datos siesta no esta creada
from database import init_db

# importa las variables donde se encuentra toda la información de tdp(tratamiento de
# datos personales), información del autor e información de la app.
from info import tdp, info_control_total, info_sobre_autor


#Función de streamlit para utilizar la página completa
st.set_page_config(page_title="Control Total", layout="wide", page_icon="🐳")

def main():
    """Función principal que controla el flujo de la aplicación.

    Args:
        None

    Returns:
        None
    """

    # Asegura de que todas las tablas estén creadas al iniciar la aplicación
    init_db()

    # Claves de estado de sesión necesarias
    if 'confirmation' not in st.session_state:
        st.session_state.confirmation = False
    if 'update_data' not in st.session_state:
        st.session_state.update_data = {}
    if 'confirmation_delete' not in st.session_state:
        st.session_state.confirmation_delete = False
    if 'delete_id' not in st.session_state:
        st.session_state.delete_id = None

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

    # Función de streamlit para dividir la página en columnas
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("Control Total")
        username = st.text_input("Nombre de Usuario")
        password = st.text_input("Contraseña", type="password")
        user = verify_user(username, password, check_only=True)

        if user:
            if user.tdp == "No Aceptado":
                # Aquí usamos Markdown para mostrar las políticas
                policies_text = (tdp)
                st.markdown(policies_text)

                accept_policies = st.checkbox(
                    "Acepto las políticas de tratamiento de datos personales al iniciar sesión.")
                if st.button("Ingresar"):
                    if accept_policies:
                        update_tdp_status(user.id, "Aceptado")
                        st.session_state['user'] = user
                        st.experimental_rerun()
                    else:
                        st.error("Debes aceptar las políticas de tratamiento de datos personales para iniciar sesión.")
                        st.stop()
            else:
                if st.button("Ingresar"):
                    st.session_state['user'] = user
                    st.experimental_rerun()
        else:
            if st.button("Ingresar"):
                st.error("Usuario o contraseña incorrectos.")


def main_menu(user):
    """Crea y muestra el menú principal para la navegación de la aplicación.

    Args:
        user (dict): Diccionario que contiene la información del usuario autenticado.

    Returns:
        None
    """
    # Condicionales para mostrar el menú admin o el menú empleado
    if user.role == "Admin":
        with st.sidebar:
            selected = option_menu(
                None,
                ["Control Total", "Admin", "Ventas y Facturación", "Gestión de inventarios",
                 "Análisis estadísticos", "Domicilios", "Sobre el Autor"],
                icons=["cast", "person-circle", "currency-dollar", "archive", "graph-up", "truck", "info-circle"],
                menu_icon="list",
                default_index=0
            )
            if st.button("Cerrar Sesión"):
                logout()

        if selected == 'Control Total':
            st.markdown(info_control_total)

        if selected == 'Admin':
            admin_menu()

        if selected == 'Gestión de inventarios':
            inventory_management_menu()

        if selected == 'Ventas y Facturación':
            sales_menu()

        if selected == 'Sobre el Autor':
            st.markdown(info_sobre_autor)

    elif user.role == "Empleado":
        with st.sidebar:
            selected = option_menu(
                None,
                ["Control Total", "Ventas y Facturación", "Gestión de inventarios",
                 "Análisis estadísticos", "Domicilios", "Sobre el Autor"],
                icons=["cast","currency-dollar", "archive", "graph-up",
                       "truck", "info-circle"],
                menu_icon="cast",
                default_index=0
            )
            if st.button("Cerrar Sesión"):
                logout()

        if selected == 'Control Total':
            st.markdown(info_control_total)

        if selected == 'Gestión de inventarios':
            inventory_management_menu()

        if selected == 'Ventas y Facturación':
            with st.expander("Opciones de Ventas y Facturación"):
                sales_client_menu = st.radio(
                    "Selecciona una opción",
                    ('Ventas', 'Clientes')
                )
                if sales_client_menu == 'Clientes':
                    client_management_menu()

        if selected == 'Sobre el Autor':
            st.markdown(info_sobre_autor)


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
    # Menu para la gestión de usuarios
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
    # Formulario para crear un nuevo usuario.
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
    # Restricción para crear un usuario
    if len(username) < 5:
        st.error("El nombre de usuario debe tener al menos 5 caracteres.")
    # Restricción para crear una contraseña
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
    """Formulario para buscar usuarios existentes en la base de datos usando ID o nombre.

    Args:
        None

    Returns:
        None
    """
    with st.form("Buscar Usuario"):
        search_query = st.text_input("Introduzca ID o nombre del usuario a buscar")
        submitted = st.form_submit_button("Buscar")
        if submitted:
            user = search_users(search_query)
            if user:
                # Muestra la información detallada del usuario encontrado
                st.write(f"ID: {user.id}, Nombre: {user.full_name}, Usuario: {user.username}, Rol: {user.role}, Teléfono: {user.phone_number}")
            else:
                st.error("No se encontró ningún usuario con ese criterio.")


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
                f"|ID: {user.id}| |Nombre: {user.full_name}| "
                f"|Usuario: {user.username}| |Rol: {user.role}| |Teléfono: {user.phone_number}|")
    else:
        st.write("No se encontraron usuarios")


def update_user_form():
    """Formulario para actualizar la información de un usuario existente."""
    # Utilizamos el estado de la sesión para almacenar temporalmente la información del usuario
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None

    with st.form("Buscar Usuario"):
        search_query = st.text_input("Nombre o ID del Usuario a actualizar", help="Escriba el ID o nombre del usuario para buscar")
        search_button = st.form_submit_button("Buscar Usuario")

        if search_button and search_query:
            user_info = search_users(search_query)
            if user_info:
                st.session_state.user_info = user_info
                st.success(f"Usuario encontrado: {user_info.full_name} (ID: {user_info.id})")
            else:
                st.error("Usuario no encontrado. Por favor, verifica el ID o nombre e intenta de nuevo.")
                st.session_state.user_info = None

    if st.session_state.user_info:
        user_info = st.session_state.user_info
        with st.form("Actualizar Usuario"):
            new_username = st.text_input("Nuevo Nombre de Usuario", placeholder="Dejar en blanco si no desea cambiar")
            new_password = st.text_input("Nueva Contraseña", type="password", placeholder="Dejar en blanco si no desea cambiar")
            new_role = st.selectbox("Nuevo Rol", ["", "Admin", "Empleado"], index=0)
            new_full_name = st.text_input("Nuevo Nombre Completo", placeholder="Dejar en blanco si no desea cambiar")
            new_phone_number = st.text_input("Nuevo Número de Celular", placeholder="Dejar en blanco si no desea cambiar")
            submitted = st.form_submit_button("Actualizar")

            if submitted:
                confirm = st.checkbox("Confirmar actualización", value=False)
                if confirm and st.button("Confirmar Cambios"):
                    result = update_user(
                        user_info.id,
                        new_username if new_username else None,
                        new_password if new_password else None,
                        new_role if new_role and new_role != user_info.role else None,
                        new_full_name if new_full_name else None,
                        new_phone_number if new_phone_number else None
                    )
                    if "éxito" in result:
                        st.success(result)
                        st.session_state.user_info = None  # Reset user_info after update
                    else:
                        st.error(result)



def delete_user_form():
    """Formulario para eliminar un usuario existente.

    Args:
        None

    Returns:
        None
    """
    st.write("Eliminar Usuario")
    del_id = st.number_input("ID del Usuario a eliminar", step=1)
    delete_submitted = st.button("Eliminar Usuario")

    if delete_submitted:
        # Guardar el ID del usuario a eliminar en el estado de la sesión
        st.session_state.delete_id = del_id
        # Marca para mostrar los botones de confirmación
        st.session_state.confirmation_delete = True

    if st.session_state.get('confirmation_delete'):
        st.write("¿Estás seguro de que quieres eliminar este usuario?")
        if st.button("Sí, eliminar"):
            # Llamar a la función de eliminación con el ID guardado y manejar la respuesta
            result = delete_user(st.session_state.delete_id)
            if "éxito" in result:
                st.success(result)
                # Restablecer la confirmación
                st.session_state.confirmation_delete = False
                # Limpiar el ID almacenado
                del st.session_state.delete_id
            else:
                st.error(result)
        elif st.button("No, cancelar"):
            st.write("Eliminación cancelada.")
            # Restablecer la confirmación
            st.session_state.confirmation_delete = False
            # Limpiar el ID almacenado
            del st.session_state.delete_id


def inventory_management_menu():
    """Muestra el menú de gestión de inventarios para buscar, modificar
     agregar productos, y eliminar productos.

     Args:
        None

    Returns:
        None
    """
    selected = option_menu(
        None,
        ["Buscar Producto", "Modificar Producto", "Agregar Producto", "Eliminar Producto"],
        icons=["search", "pencil-square", "plus-circle", "trash"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if selected == "Buscar Producto":
        search_product_form()
    elif selected == "Modificar Producto":
        update_product_form()
    elif selected == "Agregar Producto":
        add_product_form()
    elif selected == "Eliminar Producto":
        delete_product_form()

def search_product_form():
    """Formulario para buscar productos por nombre.

    Args:
        None

    Returns:
        None
    """
    with st.form("Buscar Producto"):
        search_query = st.text_input("Nombre del Producto a buscar")
        submitted = st.form_submit_button("Buscar")
        if submitted:
            products = search_products(search_query)
            #Toma cada una de la información de los productos y la muestra
            for product in products:
                st.write(f"|ID: {product.id}| |Nombre: {product.name}| |Marca: {product.brand}| "
                         f"|Categoría: {product.category}| |Subcategoría: {product.subcategory}|"
                         f"|Precio: ${product.price}| |Cantidad: {product.quantity}|")


def update_product_form():
    """Formulario para modificar información de un producto existente.

    Args:
        None

    Returns:
        None
    """
    with st.form("Modificar Producto"):
        product_id = st.number_input("ID del Producto a modificar", step=1, format="%d")
        new_name = st.text_input("Nuevo Nombre del Producto", placeholder="Dejar en "
                                 "blanco si no desea cambiar")
        new_brand = st.text_input("Nueva Marca del Producto", placeholder="Dejar en "
                                  "blanco si no desea cambiar")
        new_category = st.text_input("Nueva Categoría del Producto", placeholder="Dejar en "
                                     "blanco si no desea cambiar")
        new_subcategory = st.text_input("Nueva Subcategoría del Producto",
                                        placeholder="Dejar en blanco si no desea cambiar")
        new_price = st.number_input("Nuevo Precio del Producto", format="%.2f",
                                    help="Dejar en blanco para mantener el precio actual", value=0.0)
        inventory_adjustment = st.number_input("Ajuste de Inventario (positivo para añadir,"
                                               " negativo para reducir)",
                                               value=0, format="%d", step=1)
        submitted = st.form_submit_button("Actualizar")

        # Se verifica el cambio únicamente de los campos modificados
        if submitted:
            result = update_product(
                product_id,
                new_name if new_name else None,
                new_brand if new_brand else None,
                new_category if new_category else None,
                new_subcategory if new_subcategory else None,
                new_price if new_price != 0.0 else None,
                inventory_adjustment if inventory_adjustment else None
            )
            if "éxito" in result:
                st.success(result)
            else:
                st.error(result)

def add_product_form():
    """Formulario para añadir un nuevo producto.

    Args:
        None

    Returns:
        None
    """
    with st.form("Agregar Producto"):
        name = st.text_input("Nombre del Producto")
        brand = st.text_input("Marca del Producto")
        category = st.text_input("Categoría del Producto")
        subcategory = st.text_input("Subcategoría del Producto")
        price = st.number_input("Precio del Producto", min_value=0.01, format="%.2f")
        quantity = st.number_input("Cantidad del Producto", min_value=0, step=1)
        submitted = st.form_submit_button("Agregar")

        if submitted:
            result = add_product(name, brand, category, subcategory, price, quantity)
            if "éxito" in result:
                st.success(result)
            else:
                st.error(result)

def delete_product_form():
    """Formulario para eliminar un producto existente.

    Args:
        None

    Returns:
        None
    """
    with st.form("Eliminar Producto"):
        product_id = st.number_input("ID del Producto a eliminar", step=1, min_value=1)
        submitted = st.form_submit_button("Eliminar Producto")

    if submitted:
        # Guardar el ID del producto a eliminar en el estado de la sesión
        st.session_state.delete_id = product_id
        # Marca para mostrar los botones de confirmación
        st.session_state.confirmation_delete = True

    if st.session_state.get('confirmation_delete'):
        st.write("¿Estás seguro de que quieres eliminar este producto?")
        if st.button("Sí, eliminar"):
            # Llamar a la función de eliminación con el ID guardado y manejar la respuesta
            result = delete_product(st.session_state.delete_id)
            if "éxito" in result:
                st.success(result)
                # Restablecer la confirmación
                st.session_state.confirmation_delete = False
                # Limpiar el ID almacenado
                del st.session_state.delete_id
            else:
                st.error(result)
        elif st.button("No, cancelar"):
            st.write("Eliminación cancelada.")
            # Restablecer la confirmación
            st.session_state.confirmation_delete = False
            # Limpiar el ID almacenado
            del st.session_state.delete_id


def sales_menu():
    selected = option_menu(
        menu_title=None,  # Sin título para el menú
        options=["Ventas", "Clientes"],  # Opciones del menú
        icons=["cash", "people"],  # Íconos para cada opción
        orientation="horizontal",
        default_index=0,  # Ventas como pestaña predeterminada
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "18px"},
            "nav-link": {"font-size": "13px", "text-align": "left", "margin": "0px", "padding": "8px",
                         "border-radius": "0", "background-color": "#25d366", "color": "white"},
            "nav-link-selected": {"background-color": "green"
                                  },
        }
    )

    if selected == "Ventas":
        st.subheader("Gestión de Ventas")
        # Aquí agregar funciones o formularios para manejar las ventas
    elif selected == "Clientes":
        client_management_menu()

def client_management_menu():
    selected = option_menu(
        None,
        ["Crear Cliente", "Buscar Cliente", "Actualizar Cliente", "Eliminar Cliente"],
        icons=["plus-circle", "search", "pencil-square", "trash"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if selected == 'Crear Cliente':
        create_client_form()
    elif selected == 'Buscar Cliente':
        search_client_form()
    elif selected == 'Actualizar Cliente':
        update_client_form()
    elif selected == 'Eliminar Cliente':
        delete_client_form()

def create_client_form():
    with st.form("Crear Cliente"):
        nombre = st.text_input("Nombre Completo")
        direccion = st.text_input("Dirección")
        telefono = st.text_input("Teléfono")
        cedula = st.text_input("Cédula")
        credito = st.number_input("Crédito", format="%f", step=0.01, value=0.00)

        submitted = st.form_submit_button("Crear Cliente")
        if submitted:
            result = create_client(nombre, direccion, telefono, cedula, credito)
            if "éxito" in result:
                st.success(result)
            else:
                st.error(result)

def search_client_form():
    with st.form("Buscar Cliente"):
        search_query = st.text_input("Introduzca el nombre o cédula del cliente a buscar")
        submitted = st.form_submit_button("Buscar Cliente")
        if submitted:
            clients = search_clients(search_query)
            if clients:
                for client in clients:
                    st.write(f"Nombre: {client.nombre}, Dirección: {client.direccion}, Teléfono: {client.telefono}, Cédula: {client.cedula}, Crédito: {client.credito}")
            else:
                st.write("No se encontraron clientes")

def update_client_form():
    with st.form("Actualizar Cliente"):
        cedula = st.text_input("Cédula del Cliente a actualizar", help="Usa la cédula para buscar el cliente")
        new_nombre = st.text_input("Nuevo Nombre", placeholder="Dejar en blanco si no desea cambiar")
        new_direccion = st.text_input("Nueva Dirección", placeholder="Dejar en blanco si no desea cambiar")
        new_telefono = st.text_input("Nuevo Teléfono", placeholder="Dejar en blanco si no desea cambiar")
        new_credito = st.number_input("Nuevo Crédito", format="%.2f", value=0.0, help="Dejar en blanco para mantener el crédito actual")

        submitted = st.form_submit_button("Actualizar Cliente")
        if submitted:
            result = update_client(
                cedula,
                new_nombre if new_nombre else None,
                new_direccion if new_direccion else None,
                new_telefono if new_telefono else None,
                new_credito if new_credito != 0.0 else None
            )
            if "éxito" in result:
                st.success(result)
            else:
                st.error(result)


def delete_client_form():
    with st.form("Eliminar Cliente"):
        cedula = st.text_input("Cédula del Cliente a eliminar")
        submitted = st.form_submit_button("Eliminar Cliente")
        if submitted:
            result = delete_client(cedula)
            if "éxito" in result:
                st.success(result)
            else:
                st.error(result)


if __name__ == "__main__":
    main()

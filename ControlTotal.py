# Importa el módulo de Streamlit para crear aplicaciones web
import streamlit as st

# Importa la clase datetime para manejar fechas y horas
from datetime import datetime

# Importa la clase Decimal para manejo de números decimales
from decimal import Decimal

# Importa módulos y funciones para análisis de datos y visualización
import contextily as ctx
import geopandas as gpd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Importa geocodificación y manejo de errores de geocodificación
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# Importa funciones para calcular distancias y análisis estadístico
from scipy.spatial.distance import pdist, squareform
import scipy.stats as stats

# Importa módulos para manejo de geometría
from shapely.geometry import LineString, Point

# Importa opciones de menú para la navegación en la aplicación
from streamlit_option_menu import option_menu

# Importa funciones de autenticación de usuario
from auth import verify_user, update_tdp_status

# Importa funciones para la gestión de clientes
from client_management import (
    create_client, search_clients, delete_client,
    update_client_credit, update_client
)

# Importa la sesión de la base de datos
from database import Session

# Importa la función para crear la base de datos si no está creada
from database import init_db

# Importa variables con información sobre tratamiento de datos personales, autor y la app
from info import tdp, info_control_total, info_sobre_autor

# Importa los modelos Venta y Producto
from models import Venta, Product

# Importa funciones para la gestión de productos
from product_management import (
    search_products, delete_product, update_product, add_product
)

# Importa funciones para la gestión de ventas
from sales_management import create_sale

# Importa funciones para la gestión de usuarios
from user_management import (
    create_user, search_users, update_user, delete_user, generate_password
)

#Función de streamlit para utilizar la página completa
st.set_page_config(page_title="Control Total", layout="wide", page_icon="🐯")

geolocator = Nominatim(user_agent="tsp_solver")
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

def reset_sale():
    """
    Limpia el estado de la sesión para iniciar una nueva venta.

    Args:
        None

    Returns:
        None
    """
    st.session_state['current_sale'] = []
    st.session_state['selected_client'] = None
    st.session_state['cancel_sale'] = False
    st.session_state['confirm_payment'] = False


def login_page():
    """Crea y gestiona la página de inicio de sesión.

    Args:
        None

    Returns:
        None
    """

    logo_url = "https://i.ibb.co/HryLWKK/Logo-Control-Total-removebg-preview.png"
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.image(logo_url, width=200)

    with col2:
        st.title("Control Total")
        username = st.text_input("Nombre de Usuario")
        password = st.text_input("Contraseña", type="password")
        sitio = st.selectbox("Ubicación", ["Tienda", "Bodega"])
        user = verify_user(username, password, check_only=True)

        if user:
            if user.tdp == "No Aceptado":
                policies_text = tdp
                st.markdown(policies_text)
                accept_policies = st.checkbox("Acepto las políticas de tratamiento de datos personales al iniciar sesión.")
                if st.button("Ingresar"):
                    if accept_policies:
                        update_tdp_status(user.id, "Aceptado")
                        st.session_state['user'] = user
                        st.session_state['sitio'] = sitio
                        st.experimental_rerun()
                    else:
                        st.error("Debes aceptar las políticas de tratamiento de datos personales para iniciar sesión.")
                        st.stop()
            else:
                if st.button("Ingresar"):
                    st.session_state['user'] = user
                    st.session_state['sitio'] = sitio
                    st.experimental_rerun()
        else:
            if st.button("Ingresar"):
                st.error("Usuario o contraseña incorrectos.")



def main_menu(user):
    """
    Despliega el menú principal basado en el rol del usuario.

    Args:
        user (User): El objeto usuario que contiene la información del usuario.

    Returns:
        None
    """
    if user.role == "Admin":
        with st.sidebar:
            selected = option_menu(
                None,
                [
                    "Control Total", "Admin", "Ventas y Facturación",
                    "Gestión de inventarios", "Análisis estadísticos",
                    "Domicilios", "Sobre el Autor"
                ],
                icons=[
                    "cast", "person-circle", "currency-dollar", "archive",
                    "graph-up", "truck", "info-circle"
                ],
                menu_icon="list",
                default_index=0
            )
            if st.button("Cerrar Sesión"):
                logout()

        if selected == 'Control Total':
            st.markdown(info_control_total)
        elif selected == 'Admin':
            admin_menu()
        elif selected == 'Gestión de inventarios':
            inventory_management_menu()
        elif selected == 'Ventas y Facturación':
            sales_menu()
        elif selected == 'Análisis estadísticos':
            analisis_estadisticos()
        elif selected == 'Domicilios':
            dominos_menu()
        elif selected == 'Sobre el Autor':
            st.markdown(info_sobre_autor)

    elif user.role == "Empleado":
        with st.sidebar:
            selected = option_menu(
                None,
                [
                    "Ventas y Facturación", "Gestión de inventarios",
                    "Domicilios", "Sobre el Autor"
                ],
                icons=[
                    "currency-dollar", "archive", "truck", "info-circle"
                ],
                menu_icon="list",
                default_index=0
            )
            if st.button("Cerrar Sesión"):
                logout()

        if selected == 'Gestión de inventarios':
            inventory_management_menu()
        elif selected == 'Ventas y Facturación':
            sales_menu()
        elif selected == 'Domicilios':
            dominos_menu()
        elif selected == 'Sobre el Autor':
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
    """
    Formulario para actualizar la información de un usuario existente.

    Args:
        None

    Returns:
        None
    """
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
        st.session_state.confirmation = False

    # Sección de búsqueda del usuario
    with st.form("Buscar Usuario"):
        search_query = st.text_input(
            "Nombre o ID del Usuario a actualizar",
            help="Escriba el ID o nombre del usuario para buscar"
        )
        search_button = st.form_submit_button("Buscar Usuario")
        if search_button and search_query:
            user_info = search_users(search_query)
            if user_info:
                st.session_state.user_info = user_info
                st.success(
                    f"Usuario encontrado: {user_info.full_name} (ID: {user_info.id})"
                )
            else:
                st.error(
                    "Usuario no encontrado. Por favor, verifica el ID o nombre e intenta de nuevo."
                )
                st.session_state.user_info = None  # Reset user_info if not found

    # Sección para actualizar datos del usuario
    if st.session_state.user_info:
        with st.form("Actualizar Usuario"):
            new_username = st.text_input(
                "Nuevo Nombre de Usuario",
                placeholder="Dejar en blanco si no desea cambiar"
            )
            new_password = st.text_input(
                "Nueva Contraseña",
                type="password",
                placeholder="Dejar en blanco si no desea cambiar"
            )
            new_role = st.selectbox(
                "Nuevo Rol",
                ["", "Admin", "Empleado"],
                index=0
            )
            new_full_name = st.text_input(
                "Nuevo Nombre Completo",
                placeholder="Dejar en blanco si no desea cambiar"
            )
            new_phone_number = st.text_input(
                "Nuevo Número de Celular",
                placeholder="Dejar en blanco si no desea cambiar"
            )

            submitted = st.form_submit_button("Actualizar")
            if submitted:
                # Almacenar datos para confirmación
                st.session_state.update_data = {
                    "update_id": st.session_state.user_info.id,
                    "new_username": new_username,
                    "new_password": new_password,
                    "new_role": new_role,
                    "new_full_name": new_full_name,
                    "new_phone_number": new_phone_number
                }
                # Activa la confirmación
                st.session_state.confirmation = True

    # Confirmación de la actualización
    if st.session_state.confirmation:
        st.write("¿Estás seguro de que quieres actualizar este usuario?")
        if st.button("Sí, actualizar"):
            data = st.session_state.update_data
            result = update_user(
                data["update_id"],
                data["new_username"],
                data["new_password"],
                data["new_role"],
                data["new_full_name"],
                data["new_phone_number"]
            )
            if "éxito" in result:
                st.success(result)
                # Restablecer el estado después de la actualización
                st.session_state.user_info = None
                st.session_state.confirmation = False
                st.session_state.update_data = {}
            else:
                st.error(result)
        elif st.button("No, cancelar"):
            st.write("Actualización cancelada.")
            # Limpiar el estado de confirmación
            st.session_state.confirmation = False

def delete_user_form():
    """
    Formulario para eliminar un usuario.

    Args:
        None

    Returns:
        None
    """
    if 'delete_user_info' not in st.session_state:
        st.session_state.delete_user_info = None
        st.session_state.confirmation_delete_user = False

    # Sección de búsqueda del usuario para eliminar
    with st.form("Buscar Usuario para Eliminar"):
        search_query = st.text_input(
            "Nombre o ID del Usuario a eliminar",
            help="Escriba el ID o nombre del usuario para buscar"
        )
        search_button = st.form_submit_button("Buscar y Eliminar Usuario")
        if search_button and search_query:
            user_info = search_users(search_query)
            if user_info:
                st.session_state.delete_user_info = user_info
                st.write(
                    f"Usuario encontrado: {user_info.full_name} (ID: {user_info.id})"
                )
            else:
                st.error(
                    "Usuario no encontrado. Por favor, verifica el ID o nombre e "
                    "intenta de nuevo."
                )
                st.session_state.delete_user_info = None  # Reset user_info if not found

    # Confirmación de eliminación del usuario
    if st.session_state.delete_user_info:
        st.write(
            f"¿Estás seguro de que quieres eliminar a este usuario: "
            f"{st.session_state.delete_user_info.full_name}?"
        )
        if st.button("Sí, eliminar"):
            result = delete_user(st.session_state.delete_user_info.id)
            if "éxito" in result:
                st.success(result)
                st.session_state.delete_user_info = None
                st.session_state.confirmation_delete_user = False
            else:
                st.error(result)
        elif st.button("No, cancelar"):
            st.write("Eliminación cancelada.")
            st.session_state.delete_user_info = None
            st.session_state.confirmation_delete_user = False




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
    """
    Formulario para buscar productos por nombre o ID del producto.

    Args:
        None

    Returns:
        None
    """
    search_query = st.text_input("Nombre o ID del Producto a buscar")
    if st.button("Buscar Producto"):
        products = search_products(search_query)
        if products:
            st.session_state['products'] = products
        else:
            st.error("No se encontraron productos con ese criterio.")
            st.session_state['products'] = []

    if 'products' in st.session_state:
        products = st.session_state['products']
        if products:
            # Crear una tabla para mostrar la información de los productos
            product_data = []
            for product in products:
                product_data.append([
                    product.product_id, product.name, product.brand,
                    product.category, product.subcategory, product.price,
                    product.total_tienda, product.total_bodega
                ])

            df = pd.DataFrame(
                product_data,
                columns=[
                    "Product ID", "Nombre", "Marca", "Categoría", "Subcategoría",
                    "Precio", "Total en Tienda", "Total en Bodega"
                ]
            )
            st.table(df)

            for product in products:
                with st.form(f"transfer_to_tienda_form_{product.product_id}"):
                    transfer_to_tienda = st.number_input(
                        f"Cantidad a transferir de Bodega a Tienda para {product.name}",
                        min_value=0, max_value=product.total_bodega, step=1,
                        key=f"to_tienda_{product.product_id}"
                    )
                    transfer_to_tienda_submitted = st.form_submit_button(
                        "Transferir a Tienda"
                    )
                    if transfer_to_tienda_submitted:
                        result = update_product(
                            product.product_id,
                            inventory_adjustment_tienda=transfer_to_tienda,
                            inventory_adjustment_bodega=-transfer_to_tienda
                        )
                        if "éxito" in result:
                            st.success(
                                f"Transferencia a Tienda exitosa para el producto "
                                f"{product.name}."
                            )
                        else:
                            st.error(result)

                with st.form(f"transfer_to_bodega_form_{product.product_id}"):
                    transfer_to_bodega = st.number_input(
                        f"Cantidad a transferir de Tienda a Bodega para {product.name}",
                        min_value=0, max_value=product.total_tienda, step=1,
                        key=f"to_bodega_{product.product_id}"
                    )
                    transfer_to_bodega_submitted = st.form_submit_button(
                        "Transferir a Bodega"
                    )
                    if transfer_to_bodega_submitted:
                        result = update_product(
                            product.product_id,
                            inventory_adjustment_tienda=-transfer_to_bodega,
                            inventory_adjustment_bodega=transfer_to_bodega
                        )
                        if "éxito" in result:
                            st.success(
                                f"Transferencia a Bodega exitosa para el producto "
                                f"{product.name}."
                            )
                        else:
                            st.error(result)


def update_product_form():
    """
    Formulario para modificar la información de un producto existente.

    Args:
        None

    Returns:
        None
    """
    with st.form("Modificar Producto"):
        product_id = st.text_input("ID del Producto a modificar")
        new_name = st.text_input(
            "Nuevo Nombre del Producto",
            placeholder="Dejar en blanco si no desea cambiar"
        )
        new_brand = st.text_input(
            "Nueva Marca del Producto",
            placeholder="Dejar en blanco si no desea cambiar"
        )
        new_category = st.text_input(
            "Nueva Categoría del Producto",
            placeholder="Dejar en blanco si no desea cambiar"
        )
        new_subcategory = st.text_input(
            "Nueva Subcategoría del Producto",
            placeholder="Dejar en blanco si no desea cambiar"
        )
        new_price = st.number_input(
            "Nuevo Precio del Producto",
            format="%.2f",
            help="Dejar en blanco para mantener el precio actual",
            value=0.0
        )
        inventory_adjustment_tienda = st.number_input(
            "Ajuste de Inventario en Tienda (positivo para añadir, negativo para reducir)",
            value=0, format="%d", step=1
        )
        inventory_adjustment_bodega = st.number_input(
            "Ajuste de Inventario en Bodega (positivo para añadir, negativo para reducir)",
            value=0, format="%d", step=1
        )
        submitted = st.form_submit_button("Actualizar")

        if submitted:
            result = update_product(
                product_id,
                new_name if new_name else None,
                new_brand if new_brand else None,
                new_category if new_category else None,
                new_subcategory if new_subcategory else None,
                new_price if new_price != 0.0 else None,
                inventory_adjustment_tienda if inventory_adjustment_tienda else None,
                inventory_adjustment_bodega if inventory_adjustment_bodega else None
            )
            if "éxito" in result:
                st.success(result)
            else:
                st.error(result)


def add_product_form():
    """
    Formulario para agregar un nuevo producto.

    Args:
        None

    Returns:
        None
    """
    with st.form("Agregar Producto"):
        product_id = st.text_input("ID del Producto")
        name = st.text_input("Nombre del Producto")
        brand = st.text_input("Marca del Producto")
        category = st.text_input("Categoría del Producto")
        subcategory = st.text_input("Subcategoría del Producto")
        price = st.number_input(
            "Precio del Producto",
            min_value=0.01,
            format="%.2f"
        )
        cantidad = st.number_input(
            "Cantidad del Producto",
            min_value=0,
            step=1
        )
        submitted = st.form_submit_button("Agregar")

        if submitted:
            result = add_product(
                product_id, name, brand, category,
                subcategory, price, cantidad
            )
            if "éxito" in result:
                st.success(result)
            else:
                st.error(result)



def delete_product_form():
    """
    Formulario para eliminar un producto existente.

    Args:
        None

    Returns:
        None
    """
    # Inicializar variables de estado en la sesión
    if 'delete_id' not in st.session_state:
        st.session_state.delete_id = None
        st.session_state.confirmation_delete = False

    # Formulario para ingresar el ID del producto a eliminar
    with st.form("Eliminar Producto"):
        product_id = st.number_input(
            "ID del Producto a eliminar",
            step=1, min_value=1
        )
        submitted = st.form_submit_button("Eliminar Producto")
        if submitted:
            st.session_state.delete_id = str(product_id)  # Convertir a cadena
            st.session_state.confirmation_delete = True

    # Confirmación de eliminación del producto
    if st.session_state.get('confirmation_delete'):
        st.write("¿Estás seguro de que quieres eliminar este producto?")
        if st.button("Sí, eliminar"):
            try:
                result = delete_product(st.session_state.delete_id)
                if "éxito" in result:
                    st.success(result)
                    st.session_state.confirmation_delete = False
                    del st.session_state.delete_id
                else:
                    st.error(result)
            except Exception as e:
                st.error(f"Error al eliminar el producto: {e}")
        elif st.button("No, cancelar"):
            st.write("Eliminación cancelada.")
            st.session_state.confirmation_delete = False
            del st.session_state.delete_id


def sales_menu():
    """
    Muestra el menú de ventas y permite seleccionar entre la gestión de ventas
    y la gestión de clientes.

    Args:
        None

    Returns:
        None
    """
    selected = option_menu(
        menu_title=None,  # Sin título para el menú
        options=["Ventas", "Clientes"],  # Opciones del menú
        icons=["cash", "people"],  # Íconos para cada opción
        orientation="horizontal",
        default_index=0,  # Ventas como pestaña predeterminada
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "18px"},
            "nav-link": {
                "font-size": "13px", "text-align": "left", "margin": "0px",
                "padding": "8px", "border-radius": "0",
                "background-color": "#25d366", "color": "white"
            },
            "nav-link-selected": {"background-color": "green"},
        }
    )

    if selected == "Ventas":
        handle_sales()
    elif selected == "Clientes":
        client_management_menu()


def handle_sales():
    """
    Gestiona el proceso de ventas, incluyendo la búsqueda de clientes y productos,
    la adición de productos al carrito y la finalización de la venta.

    Args:
        None

    Returns:
        None
    """
    # Inicializar variables de estado en la sesión
    if 'carrito' not in st.session_state:
        st.session_state['carrito'] = []
    if 'total' not in st.session_state:
        st.session_state['total'] = 0.0

    sitio = st.session_state.get('sitio', 'Tienda')

    col1, col2, col3 = st.columns(3)
    with col1:
        cliente_registrado = st.radio(
            "Tipo de Cliente",
            ("Cliente Registrado", "Cliente No Registrado")
        )

    if cliente_registrado == "Cliente Registrado":
        with col2:
            search_query = st.text_input("Buscar Cliente por Cédula o Nombre")
            if st.button("Buscar Cliente"):
                client = search_clients(search_query)
                if client:
                    st.session_state['cliente'] = client[0]
                    st.success(f"Cliente encontrado: {client[0].nombre}")
                else:
                    st.error("Cliente no encontrado")

        with col3:
            if 'cliente' in st.session_state:
                client_info = st.session_state['cliente']
                st.write(f"**Cliente:** {client_info.nombre}")
                st.write(f"**Cédula:** {client_info.cedula}")
                st.write(f"**Crédito:** ${client_info.credito:.2f}")

    col1, col2 = st.columns(2)
    with col1:
        product_id = st.text_input("ID del Producto o Nombre del Producto")
    with col2:
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        if st.button("Agregar al Carrito"):
            products = search_products(product_id)
            if products:
                product = products[0]
                if cantidad <= product.total_tienda:
                    st.session_state['carrito'].append(
                        {'product': product, 'quantity': cantidad}
                    )
                    st.session_state['total'] += float(product.price) * cantidad
                    st.success(f"Producto {product.name} agregado al carrito")
                else:
                    st.error("Cantidad no disponible en tienda")
            else:
                st.error("Producto no encontrado")

    col1, col2 = st.columns(2)
    with col1:
        if st.session_state['carrito']:
            st.write("### Carrito de Compras")
            cart_data = []
            for i, item in enumerate(st.session_state['carrito']):
                product = item['product']
                cart_data.append([
                    product.product_id, product.name,
                    f"${product.price:.2f}", item['quantity'],
                    f"${product.price * item['quantity']:.2f}", i
                ])
            cart_df = pd.DataFrame(
                cart_data,
                columns=[
                    "Product ID", "Nombre", "Precio Unitario",
                    "Cantidad", "Importe", "Index"
                ]
            )
            st.table(cart_df.drop(columns=["Index"]))

            index_to_remove = st.number_input(
                "Índice de producto a quitar",
                min_value=0,
                max_value=len(st.session_state['carrito']) - 1,
                step=1
            )
            if st.button("Quitar Producto"):
                item_to_remove = st.session_state['carrito'].pop(index_to_remove)
                st.session_state['total'] -= (
                    float(item_to_remove['product'].price) * item_to_remove['quantity']
                )
                st.success(f"Producto {item_to_remove['product'].name} quitado del carrito")

            st.write(f"Total: ${st.session_state['total']:.2f}")

    with col2:
        if st.session_state['carrito']:
            efectivo = st.number_input("Pago en Efectivo", min_value=0.0, format="%.2f")
            transferencia = st.number_input(
                "Pago por Transferencia", min_value=0.0, format="%.2f"
            )
            if cliente_registrado == "Cliente Registrado":
                credito = st.number_input("Deuda", min_value=0.0, format="%.2f")
            else:
                credito = 0.0

            if st.button("Pagar"):
                if efectivo + transferencia + credito >= st.session_state['total']:
                    productos_vendidos = st.session_state['carrito']
                    user_id = st.session_state['user'].id
                    total_efectivo = efectivo
                    total_transferencia = transferencia
                    total_credito = credito
                    result = create_sale(
                        user_id, total_efectivo, total_transferencia,
                        productos_vendidos, total_credito, sitio
                    )

                    if cliente_registrado == "Cliente Registrado" and credito > 0:
                        cliente = st.session_state['cliente']
                        nuevo_credito = cliente.credito + Decimal(credito)
                        update_client_credit(cliente.cedula, nuevo_credito)
                        st.session_state['cliente'].credito = nuevo_credito
                        st.write(f"**Nuevo Crédito:** ${nuevo_credito:.2f}")

                    st.success(result)
                    st.session_state['carrito'] = []
                    st.session_state['total'] = 0.0
                else:
                    st.error("Pago insuficiente")

            if st.button("Cancelar Venta"):
                st.session_state['carrito'] = []
                st.session_state['total'] = 0.0
                st.success("Venta cancelada")


def create_sale(user_id, total_efectivo, total_transferencia, productos_vendidos, total_credito, sitio):
    """Registra una venta en la base de datos.

    Args:
        user_id (int): ID del usuario que realiza la venta.
        total_efectivo (float): Total pagado en efectivo.
        total_transferencia (float): Total pagado por transferencia.
        productos_vendidos (list): Lista de productos vendidos.
        total_credito (float): Total pagado en crédito.
        sitio (str): Ubicación del punto de venta (tienda o bodega).

    Returns:
        str: Mensaje indicando si la venta fue registrada con éxito o no.
    """
    session = Session()
    try:
        # Obtener la fecha y hora actual
        fecha_hora = datetime.now()

        # Preparar los datos de productos vendidos como una cadena legible con nombre y cantidad
        productos_vendidos_str = ', '.join([f"{item['product'].name}:{item['quantity']}" for item in productos_vendidos])

        # Crear una nueva venta
        new_sale = Venta(
            user_id=user_id,
            fecha_hora=fecha_hora,
            total_efectivo=total_efectivo,
            total_transferencia=total_transferencia,
            total_credito=total_credito,
            productos_vendidos=productos_vendidos_str
        )

        # Actualizar inventario
        for item in productos_vendidos:
            product = session.query(Product).filter(Product.product_id == item['product'].product_id).first()
            if sitio == 'Tienda':
                product.total_tienda -= item['quantity']
            else:
                product.total_bodega -= item['quantity']

        session.add(new_sale)
        session.commit()
        return "Venta registrada con éxito."
    except Exception as e:
        session.rollback()
        return f"Error al registrar la venta: {str(e)}"
    finally:
        session.close()

def client_management_menu():
    """
    Muestra el menú de gestión de clientes y permite seleccionar entre las
    opciones de crear, buscar, actualizar y eliminar clientes.

    Args:
        None

    Returns:
        None
    """
    selected = option_menu(
        None,
        ["Crear Cliente", "Buscar Cliente", "Actualizar Cliente", "Eliminar Cliente"],
        icons=["plus-circle", "search", "pencil-square", "trash"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    # Llamar a la función correspondiente según la opción seleccionada
    if selected == 'Crear Cliente':
        create_client_form()
    elif selected == 'Buscar Cliente':
        search_client_form()
    elif selected == 'Actualizar Cliente':
        update_client_form()
    elif selected == 'Eliminar Cliente':
        delete_client_form()


def create_client_form():
    """
    Formulario para crear un nuevo cliente.

    Args:
        None

    Returns:
        None
    """
    with st.form("Crear Cliente"):
        nombre = st.text_input("Nombre Completo")
        direccion = st.text_input("Dirección")
        telefono = st.text_input("Teléfono")
        cedula = st.text_input("Cédula")
        credito = st.number_input(
            "Crédito",
            format="%f",
            step=0.01,
            value=0.00
        )

        submitted = st.form_submit_button("Crear Cliente")
        if submitted:
            result = create_client(nombre, direccion, telefono, cedula, credito)
            if "éxito" in result:
                st.success(result)
            else:
                st.error(result)


def search_client_form():
    """
    Formulario para buscar un cliente y gestionar el abono a su crédito.

    Args:
        None

    Returns:
        None
    """
    # Inicializar variables de estado en la sesión
    if 'cliente_seleccionado' not in st.session_state:
        st.session_state['cliente_seleccionado'] = None
    if 'abono' not in st.session_state:
        st.session_state['abono'] = 0.0
    if 'confirmar_abono' not in st.session_state:
        st.session_state['confirmar_abono'] = False

    # Entrada de búsqueda del cliente
    search_query = st.text_input("Introduzca el nombre o cédula del cliente a buscar")
    if st.button("Buscar Cliente"):
        clients = search_clients(search_query)
        if clients:
            if len(clients) == 1:
                st.session_state['cliente_seleccionado'] = clients[0]
            else:
                st.session_state['cliente_seleccionado'] = None
                st.error("Por favor, refine su búsqueda para obtener un único cliente.")

            # Mostrar la información de los clientes encontrados
            client_data = []
            for client in clients:
                client_data.append([
                    client.nombre, client.direccion, client.telefono, client.cedula,
                    f"${client.credito:.2f}"
                ])
            df = pd.DataFrame(
                client_data,
                columns=["Nombre", "Dirección", "Teléfono", "Cédula", "Crédito"]
            )
            st.table(df)
        else:
            st.error("No se encontraron clientes")

    # Gestión del abono al crédito del cliente seleccionado
    if st.session_state['cliente_seleccionado']:
        cliente = st.session_state['cliente_seleccionado']
        st.session_state['abono'] = st.number_input(
            "Cantidad a abonar al crédito",
            min_value=0.0,
            format="%.2f"
        )

        if st.button("Abonar al Crédito"):
            st.session_state['confirmar_abono'] = True

    # Confirmación del abono
    if st.session_state['confirmar_abono']:
        if st.button("Confirmar Abono"):
            cliente = st.session_state['cliente_seleccionado']
            nuevo_credito = Decimal(cliente.credito) - Decimal(st.session_state['abono'])
            result = update_client_credit(cliente.cedula, nuevo_credito)
            st.write(result)
            st.session_state['confirmar_abono'] = False
            st.session_state['cliente_seleccionado'] = None
            st.session_state['abono'] = 0.0
        elif st.button("Cancelar"):
            st.session_state['confirmar_abono'] = False


def update_client_form():
    """
    Formulario para actualizar la información de un cliente existente.

    Args:
        None

    Returns:
        None
    """
    # Inicializar variable de estado en la sesión
    if 'cliente_seleccionado' not in st.session_state:
        st.session_state['cliente_seleccionado'] = None

    # Entrada de búsqueda del cliente por cédula
    search_query = st.text_input(
        "Cédula del Cliente a actualizar",
        help="Usa la cédula para buscar el cliente"
    )
    if st.button("Buscar Cliente"):
        clients = search_clients(search_query)
        if clients:
            st.session_state['cliente_seleccionado'] = clients[0]
            st.success(f"Cliente encontrado: {clients[0].nombre}")
        else:
            st.error(
                "Cliente no encontrado. Por favor, verifica la cédula e intenta de nuevo."
            )

    # Formulario para actualizar la información del cliente
    if st.session_state['cliente_seleccionado']:
        cliente = st.session_state['cliente_seleccionado']
        new_nombre = st.text_input(
            "Nuevo Nombre",
            value=cliente.nombre,
            placeholder="Dejar en blanco si no desea cambiar"
        )
        new_direccion = st.text_input(
            "Nueva Dirección",
            value=cliente.direccion,
            placeholder="Dejar en blanco si no desea cambiar"
        )
        new_telefono = st.text_input(
            "Nuevo Teléfono",
            value=cliente.telefono,
            placeholder="Dejar en blanco si no desea cambiar"
        )
        new_credito = st.number_input(
            "Nuevo Crédito",
            value=float(cliente.credito),
            format="%.2f",
            help="Dejar en blanco para mantener el crédito actual"
        )

        # Botón para actualizar la información del cliente
        if st.button("Actualizar Cliente"):
            result = update_client(
                cliente.cedula,
                new_nombre if new_nombre else None,
                new_direccion if new_direccion else None,
                new_telefono if new_telefono else None,
                Decimal(new_credito) if new_credito != 0.0 else None
            )
            st.write(result)
            if "éxito" in result:
                st.session_state['cliente_seleccionado'] = None
            else:
                st.error("Hubo un error al actualizar el cliente.")


def delete_client_form():
    """
    Formulario para eliminar un cliente existente.

    Args:
        None

    Returns:
        None
    """
    with st.form("Eliminar Cliente"):
        cedula = st.text_input("Cédula del Cliente a eliminar")
        submitted = st.form_submit_button("Eliminar Cliente")

        # Si se envía el formulario, se intenta eliminar el cliente
        if submitted:
            result = delete_client(cedula)
            if "éxito" in result:
                st.success(result)
            else:
                st.error(result)


def dominos_menu():
    """
    Muestra el menú para la optimización de rutas de entrega y permite calcular
    la ruta óptima para varias direcciones de entrega.

    Args:
        None

    Returns:
        None
    """
    st.title("Optimización de Ruta de Entrega")

    # Dirección de inicio fija
    start_address = "Cl. 1 #77-129, Medellin, Colombia"
    st.write(f"Dirección de inicio: {start_address}")

    # Ingreso de direcciones manualmente
    address_inputs = []
    num_addresses = st.number_input(
        "Número de direcciones de entrega",
        min_value=1,
        max_value=10,
        step=1
    )

    for i in range(num_addresses):
        address = st.text_input(f"Dirección {i + 1}", key=f"address_{i}")
        address_inputs.append(address)

    # Botón para calcular la ruta
    if st.button("Calcular Ruta"):
        addresses = [start_address] + address_inputs

        try:
            # Obtener coordenadas de las direcciones
            locations = []
            geolocator = Nominatim(user_agent="tsp_solver")
            for address in addresses:
                coordenadas = obtener_coordenadas(geolocator, address)
                if coordenadas:
                    locations.append(coordenadas)
                else:
                    st.error(f"No se pudieron obtener coordenadas para: {address}")
                    return

            # Convertir las coordenadas a DataFrame
            df_locations = pd.DataFrame(
                locations,
                columns=['Latitude', 'Longitude']
            )

            # Calcular la matriz de distancias
            coords = df_locations.to_numpy()
            distance_matrix = squareform(pdist(coords, metric='euclidean'))

            # Resolver el TSP usando la heurística de vecino más cercano
            tour = nearest_neighbor(distance_matrix)
            tour.append(tour[0])  # Volver al punto de partida

            # Mostrar el tour de manera ordenada
            tour_df = pd.DataFrame({
                "Número": tour,  # Usar los índices del tour directamente
                "Dirección": [addresses[i] for i in tour]
            })

            st.dataframe(tour_df)
            plot_geopandas_map(df_locations, tour)
        except Exception as e:
            st.error(f"Error al calcular la ruta: {e}")


def nearest_neighbor(distance_matrix):
    """
    Resuelve el problema del viajante (TSP) utilizando la heurística del
    vecino más cercano.

    Args:
        distance_matrix (ndarray): Matriz de distancias entre las ubicaciones.

    Returns:
        list: Orden de las ubicaciones visitadas en el tour.
    """
    n = distance_matrix.shape[0]
    visited = [False] * n
    tour = [0]
    visited[0] = True

    for _ in range(n - 1):
        last_visited = tour[-1]
        # Encontrar el vecino más cercano no visitado
        nearest = np.argmin(
            [
                distance_matrix[last_visited][j] if not visited[j]
                else np.inf for j in range(n)
            ]
        )
        tour.append(nearest)
        visited[nearest] = True

    return tour


def plot_route(df_locations, tour):
    """
    Plotea la ruta de entrega en un mapa utilizando las coordenadas
    de las ubicaciones y el orden del tour.

    Args:
        df_locations (DataFrame): DataFrame con las coordenadas de las
        ubicaciones.
        tour (list): Lista con el orden de las ubicaciones en el tour.

    Returns:
        None
    """
    try:
        # Crear la ruta a partir del tour
        route = [
            (df_locations.Longitude[i], df_locations.Latitude[i])
            for i in tour
        ]

        # Crear la línea de la ruta
        line = LineString(route)

        # Plotear la ruta y los puntos
        fig, ax = plt.subplots(figsize=(10, 10))  # Tamaño del mapa

        # Plotear los puntos de la ruta
        for lon, lat in route:
            ax.plot(lon, lat, 'ro', markersize=5)

        # Destacar el punto de inicio
        inicio = route[0]
        ax.plot(inicio[0], inicio[1], 'go', markersize=10)

        # Añadir la línea de la ruta
        x, y = line.xy
        ax.plot(x, y, color='blue')

        # Añadir el mapa base
        ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)

        # Ocultar las etiquetas de los ejes
        ax.set_xticks([])
        ax.set_yticks([])

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error al plotear la ruta: {e}")


def ajustar_fecha(fecha):
    """
    Ajusta la fecha y hora restando 5 horas.

    Args:
        fecha (datetime): La fecha y hora original.

    Returns:
        datetime: La fecha y hora ajustada.
    """
    return fecha - pd.Timedelta(hours=5)


def cargar_datos_ventas():
    """
    Carga los datos de ventas desde la base de datos y los convierte en un
    DataFrame de pandas.

    Args:
        None

    Returns:
        DataFrame: Un DataFrame de pandas con los datos de ventas.
    """
    session = Session()
    ventas = session.query(Venta).all()
    session.close()

    # Convertir los datos de ventas a un DataFrame
    return pd.DataFrame([{
        'user_id': venta.user_id,
        'fecha_hora': ajustar_fecha(venta.fecha_hora),
        'total_efectivo': float(venta.total_efectivo),
        'total_transferencia': float(venta.total_transferencia),
        'total_credito': float(venta.total_credito),
        'productos_vendidos': venta.productos_vendidos
    } for venta in ventas])


def calcular_estadisticas(datos_ventas):
    """
    Calcula estadísticas descriptivas de las ventas.

    Args:
        datos_ventas (DataFrame): DataFrame con los datos de ventas.

    Returns:
        dict: Diccionario con las estadísticas calculadas.
    """
    ventas = datos_ventas[
        ['total_efectivo', 'total_transferencia', 'total_credito']
    ].to_numpy()
    estadisticas = {
        'media_efectivo': np.mean(ventas[:, 0]),
        'media_transferencia': np.mean(ventas[:, 1]),
        'media_credito': np.mean(ventas[:, 2]),
        'desviacion_efectivo': np.std(ventas[:, 0]),
        'desviacion_transferencia': np.std(ventas[:, 1]),
        'desviacion_credito': np.std(ventas[:, 2]),
    }
    return estadisticas

def mostrar_estadisticas(datos_ventas):
    """
    Muestra las estadísticas descriptivas de las ventas.

    Args:
        datos_ventas (DataFrame): DataFrame con los datos de ventas.

    Returns:
        None
    """
    estadisticas = calcular_estadisticas(datos_ventas)
    st.write("## Estadísticas Descriptivas")
    st.write(f"Media Efectivo: ${estadisticas['media_efectivo']:.2f}")
    st.write(f"Media Transferencia: ${estadisticas['media_transferencia']:.2f}")
    st.write(f"Media Crédito: ${estadisticas['media_credito']:.2f}")
    st.write(
        f"Desviación Estándar Efectivo: ${estadisticas['desviacion_efectivo']:.2f}"
    )
    st.write(
        f"Desviación Estándar Transferencia: ${estadisticas['desviacion_transferencia']:.2f}"
    )
    st.write(
        f"Desviación Estándar Crédito: ${estadisticas['desviacion_credito']:.2f}"
    )

def prueba_hipotesis(datos_ventas):
    """
    Realiza una prueba de hipótesis para comparar las ventas en efectivo y
    por transferencia.

    Args:
        datos_ventas (DataFrame): DataFrame con los datos de ventas.

    Returns:
        None
    """
    ventas_efectivo = datos_ventas['total_efectivo']
    ventas_transferencia = datos_ventas['total_transferencia']
    t_stat, p_value = stats.ttest_ind(ventas_efectivo, ventas_transferencia)

    st.write("## Prueba de Hipótesis")
    st.write(f"T-statistic: {t_stat:.2f}")
    st.write(f"P-value: {p_value:.4f}")
    if p_value < 0.05:
        st.write(
            "Rechazamos la hipótesis nula. Las ventas en efectivo y transferencia "
            "son significativamente diferentes."
        )
    else:
        st.write(
            "No rechazamos la hipótesis nula. No hay diferencias significativas "
            "entre las ventas en efectivo y transferencia."
        )

def analisis_estadisticos():
    """
    Muestra el menú de análisis estadísticos y llama a las funciones
    correspondientes según la opción seleccionada.

    Args:
        None

    Returns:
        None
    """
    datos_ventas = cargar_datos_ventas()

    selected = option_menu(
        None,
        [
            "Ventas por Día", "Método de Pago", "Cuadre de Caja",
            "Estadísticas Descriptivas", "Prueba de Hipótesis"
        ],
        icons=["calendar", "credit-card", "cash-stack", "bar-chart", "flask"],
        menu_icon="graph-up",
        default_index=0,
        orientation="horizontal"
    )

    if selected == "Ventas por Día":
        ventas_por_dia(datos_ventas)
    elif selected == "Método de Pago":
        metodo_de_pago(datos_ventas)
    elif selected == "Cuadre de Caja":
        cuadre_de_caja(datos_ventas)
    elif selected == "Estadísticas Descriptivas":
        mostrar_estadisticas(datos_ventas)
    elif selected == "Prueba de Hipótesis":
        prueba_hipotesis(datos_ventas)

def ventas_por_dia(datos_ventas):
    """
    Muestra un análisis de ventas por día con selección de rangos de fechas.

    Args:
        datos_ventas (DataFrame): DataFrame con los datos de ventas.

    Returns:
        None
    """
    fecha_inicio = st.date_input(
        "Selecciona la fecha de inicio",
        value=pd.to_datetime("today") - pd.Timedelta(days=7)
    )
    fecha_fin = st.date_input(
        "Selecciona la fecha de fin",
        value=pd.to_datetime("today")
    )

    datos_ventas['fecha'] = datos_ventas['fecha_hora'].dt.date
    ventas_rango = datos_ventas[
        (datos_ventas['fecha'] >= fecha_inicio) &
        (datos_ventas['fecha'] <= fecha_fin)
    ]

    if ventas_rango.empty:
        st.write(
            "No se registraron ventas en el rango de fechas seleccionado o la "
            "fecha es futura."
        )
    else:
        ventas_dia = ventas_rango.groupby('fecha').agg({
            'total_efectivo': 'sum',
            'total_transferencia': 'sum',
            'total_credito': 'sum'
        }).reset_index()

        ventas_dia['total_ventas'] = (
            ventas_dia['total_efectivo'] + ventas_dia['total_transferencia'] +
            ventas_dia['total_credito']
        )

        st.write(f"## Ventas desde {fecha_inicio} hasta {fecha_fin}")
        fig, ax = plt.subplots()
        ax.bar(ventas_dia['fecha'], ventas_dia['total_ventas'], color='skyblue')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Total Ventas')
        ax.set_title('Ventas por Día')

        # Ajustar el formato de las etiquetas de fecha y los precios
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        fig.autofmt_xdate(rotation=45)
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, loc: "${:,.2f}".format(x))
        )

        st.pyplot(fig)

def metodo_de_pago(datos_ventas):
    """
    Muestra un análisis de los métodos de pago con selección de fecha.

    Args:
        datos_ventas (DataFrame): DataFrame con los datos de ventas.

    Returns:
        None
    """
    fecha_seleccionada = st.date_input(
        "Selecciona una fecha",
        value=pd.to_datetime("today")
    )
    datos_ventas['fecha'] = datos_ventas['fecha_hora'].dt.date
    metodos_pago = datos_ventas[datos_ventas['fecha'] == fecha_seleccionada][
        ['total_efectivo', 'total_transferencia', 'total_credito']
    ].sum()

    if metodos_pago.sum() == 0:
        st.write(
            "No se registraron ventas en la fecha seleccionada o la fecha es futura."
        )
    else:
        st.write(f"## Método de Pago del día {fecha_seleccionada}")
        fig, ax = plt.subplots()
        ax.pie(
            metodos_pago, labels=metodos_pago.index,
            autopct='%1.1f%%', startangle=90
        )
        ax.axis('equal')
        st.pyplot(fig)

def cuadre_de_caja(datos_ventas):
    """
    Realiza el cuadre de caja del negocio por ID de empleado y selección de
    fecha.

    Args:
        datos_ventas (DataFrame): DataFrame con los datos de ventas.

    Returns:
        None
    """
    fecha_seleccionada = st.date_input(
        "Selecciona una fecha",
        value=pd.to_datetime("today")
    )
    empleado_id = st.number_input("ID del Empleado", min_value=1, step=1)
    dinero_inicial = st.number_input(
        "Dinero inicial del día",
        min_value=0.0,
        format="%.2f"
    )

    datos_ventas['fecha'] = datos_ventas['fecha_hora'].dt.date
    ventas_empleado = datos_ventas[
        (datos_ventas['fecha'] == fecha_seleccionada) &
        (datos_ventas['user_id'] == empleado_id)
    ]

    if ventas_empleado.empty:
        st.write(
            "No se registraron ventas en la fecha seleccionada para el empleado o "
            "la fecha es futura."
        )
    else:
        suma_efectivo = ventas_empleado['total_efectivo'].sum()
        suma_transferencia = ventas_empleado['total_transferencia'].sum()
        suma_credito = ventas_empleado['total_credito'].sum()
        suma_total = suma_efectivo + suma_transferencia + suma_credito
        suma_efectivo_transferencia = suma_efectivo + suma_transferencia + dinero_inicial

        st.write(
            f"## Cuadre de Caja del día {fecha_seleccionada} para el Empleado ID "
            f"{empleado_id}"
        )
        st.write(f"### Total Efectivo: ${suma_efectivo:.2f}")
        st.write(f"### Total Transferencia: ${suma_transferencia:.2f}")
        st.write(f"### Total Crédito: ${suma_credito:.2f}")
        st.write(f"### Suma Total: ${suma_total:.2f}")
        st.write(
            f"### Efectivo + Transferencia + Dinero Inicial: "
            f"${suma_efectivo_transferencia:.2f}"
        )

def visualizar_rutas(locations):
    """
    Visualiza las rutas de entrega en un mapa utilizando las coordenadas.

    Args:
        locations (list): Lista de tuplas con las coordenadas (latitud, longitud).

    Returns:
        None
    """
    try:
        # Crear la ruta como una LineString
        ruta = LineString([(lon, lat) for lat, lon in locations])

        # Plotear los puntos y la ruta
        fig, ax = plt.subplots(figsize=(10, 10))

        for lat, lon in locations:
            ax.plot(lon, lat, 'ro', markersize=5)

        # Destacar el punto de inicio
        inicio = locations[0]
        ax.plot(inicio[1], inicio[0], 'go', markersize=10)

        # Añadir la línea de la ruta
        x, y = ruta.xy
        ax.plot(x, y, color='blue')

        # Añadir el mapa base
        ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)

        # Ocultar las etiquetas de los ejes
        ax.set_xticks([])
        ax.set_yticks([])

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error al visualizar las rutas: {e}")

def obtener_coordenadas(geolocator, direccion, max_reintentos=3):
    """
    Obtiene las coordenadas (latitud y longitud) de una dirección utilizando
    un geolocalizador.

    Args:
        geolocator (Geolocator): Objeto geolocalizador.
        direccion (str): Dirección a geolocalizar.
        max_reintentos (int, optional): Número máximo de reintentos en caso de
        fallo. Por defecto es 3.

    Returns:
        tuple: Tupla con las coordenadas (latitud, longitud) o None si no se
        pudo obtener.
    """
    reintentos = 0
    while reintentos < max_reintentos:
        try:
            location = geolocator.geocode(direccion, timeout=10)
            if location:
                return (location.latitude, location.longitude)
            else:
                return None
        except (GeocoderTimedOut, GeocoderServiceError):
            reintentos += 1
            if reintentos == max_reintentos:
                st.error(
                    f"No se pudo geocodificar la dirección: {direccion} después "
                    f"de {max_reintentos} intentos."
                )
                return None

def plot_geopandas_map(df_locations, tour):
    """
    Visualiza las rutas de entrega en un mapa utilizando geopandas.

    Args:
        df_locations (DataFrame): DataFrame con las coordenadas de las
        ubicaciones.
        tour (list): Lista con el orden de las ubicaciones en el tour.

    Returns:
        None
    """
    try:
        # Crear la ruta utilizando el tour
        route = [
            (df_locations.Longitude[i], df_locations.Latitude[i]) for i in tour
        ]
        route.append(route[0])  # Volver al punto de partida

        # Crear puntos de geometría con geopandas
        puntos = [Point(lon, lat) for lon, lat in route]
        gdf = gpd.GeoDataFrame(geometry=puntos, crs="EPSG:4326")
        gdf = gdf.to_crs(epsg=3857)  # Convertir a la proyección adecuada

        # Crear la ruta como una LineString
        ruta = LineString(puntos)
        gdf_ruta = gpd.GeoDataFrame(geometry=[ruta], crs="EPSG:4326")
        gdf_ruta = gdf_ruta.to_crs(epsg=3857)

        # Plotear los puntos y la ruta con geopandas
        fig, ax = plt.subplots(figsize=(10, 10))
        gdf.plot(ax=ax, color='red', marker='o', markersize=5)
        gdf_ruta.plot(ax=ax, color='blue')

        # Añadir el mapa base
        ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)

        # Ocultar las etiquetas de los ejes
        ax.set_xticks([])
        ax.set_yticks([])

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)
    except Exception as e:
        st.error(f" Error al visualizar las rutas con geopandas: {e}")


if __name__ == "__main__":
    main()

# Importa la función declarative_base de SQLAlchemy para la creación de modelos ORM
from sqlalchemy.ext.declarative import declarative_base

# Importa tipos de columnas específicos de SQLAlchemy para definir propiedades de modelo
from sqlalchemy import Column, Integer, String, Numeric, DateTime, PickleType

# Importa la función relationship de SQLAlchemy para definir relaciones entre modelos
from sqlalchemy.orm import relationship

# Importa la clase datetime para manejar fechas y horas
from datetime import datetime


# Crea una instancia base para los modelos ORM, que es necesario para definir clases de modelos
Base = declarative_base()

class User(Base):
    """
    Define la estructura de la tabla 'users' para almacenar datos de usuario.

    Attributes:
        id (Column): Identificador único del usuario, clave primaria.
        username (Column): Nombre de usuario, debe ser único y no nulo.
        password (Column): Contraseña del usuario, no puede ser nula.
        role (Column): Rol del usuario en la aplicación, no puede ser nulo.
        full_name (Column): Nombre completo del usuario, no puede ser nulo.
        phone_number (Column): Número de teléfono del usuario, no puede ser nulo.
        tdp (Column): Estado de aceptación de tratamiento de datos personales.

    Args:
        None

    Returns:
        None
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    tdp = Column(String, default="No Aceptado")


class Product(Base):
    """
    Define la estructura de la tabla 'products' para almacenar datos de productos.

    Attributes:
        id (Column): Identificador único del producto, clave primaria.
        product_id (Column): Identificador del producto, debe ser único y no nulo.
        name (Column): Nombre del producto, no puede ser nulo.
        brand (Column): Marca del producto.
        category (Column): Categoría del producto, no puede ser nula.
        subcategory (Column): Subcategoría del producto.
        price (Column): Precio del producto, no puede ser nulo.
        total_tienda (Column): Cantidad del producto en tienda.
        total_bodega (Column): Cantidad del producto en bodega.

    Args:
        None

    Returns:
        None
    """
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    product_id = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    brand = Column(String)
    category = Column(String, nullable=False)
    subcategory = Column(String)
    price = Column(Numeric(10, 2), nullable=False)
    total_tienda = Column(Integer, nullable=False, default=0)
    total_bodega = Column(Integer, nullable=False, default=0)


class Cliente(Base):
    """
    Define la estructura de la tabla 'clientes' para almacenar datos de clientes.

    Attributes:
        id (Column): Identificador único del cliente, clave primaria.
        nombre (Column): Nombre del cliente, no puede ser nulo.
        direccion (Column): Dirección del cliente, no puede ser nula.
        telefono (Column): Teléfono del cliente, no puede ser nulo.
        cedula (Column): Cédula del cliente, debe ser única y no nula.
        credito (Column): Crédito del cliente.

    Args:
        None

    Returns:
        None
    """
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    cedula = Column(String, nullable=False, unique=True)
    credito = Column(Numeric(10, 2))


class Venta(Base):
    """
    Define la estructura de la tabla 'ventas' para almacenar datos de ventas.

    Attributes:
        id (Column): Identificador único de la venta, clave primaria.
        user_id (Column): Identificador del usuario que realizó la venta.
        fecha_hora (Column): Fecha y hora de la venta.
        total_efectivo (Column): Total de la venta en efectivo.
        total_transferencia (Column): Total de la venta por transferencia.
        total_credito (Column): Total de la venta a crédito.
        productos_vendidos (Column): Productos vendidos en la venta.

    Args:
        user_id (int): Identificador del usuario que realizó la venta.
        fecha_hora (datetime): Fecha y hora de la venta.
        total_efectivo (float): Total de la venta en efectivo.
        total_transferencia (float): Total de la venta por transferencia.
        total_credito (float): Total de la venta a crédito.
        productos_vendidos (str): Productos vendidos en la venta.

    Returns:
        None
    """
    __tablename__ = 'ventas'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    fecha_hora = Column(DateTime, nullable=False)
    total_efectivo = Column(Numeric(10, 2), nullable=False)
    total_transferencia = Column(Numeric(10, 2), nullable=False)
    total_credito = Column(Numeric(10, 2), nullable=False)
    productos_vendidos = Column(String, nullable=False)  # Usar String para cadenas legibles

    def __init__(self, user_id, fecha_hora, total_efectivo, total_transferencia, total_credito, productos_vendidos):
        self.user_id = user_id
        self.fecha_hora = fecha_hora
        self.total_efectivo = total_efectivo
        self.total_transferencia = total_transferencia
        self.total_credito = total_credito
        self.productos_vendidos = productos_vendidos

# Importa la función declarative_base de SQLAlchemy para la creación de modelos ORM
from sqlalchemy.ext.declarative import declarative_base

# Importa tipos de columnas específicos de SQLAlchemy para definir propiedades de modelo
from sqlalchemy import Column, Integer, String, Numeric, DateTime, PickleType

from sqlalchemy.orm import relationship

from datetime import datetime

# Crea una instancia base para los modelos ORM, que es necesario para definir clases de modelos
Base = declarative_base()

class User(Base):
    """Define la estructura de la tabla 'users' para almacenar datos de usuario.

    Attributes:
        id (Column): Identificador único del usuario, clave primaria.
        username (Column): Nombre de usuario, debe ser único y no nulo.
        password (Column): Contraseña del usuario, no puede ser nula.
        role (Column): Rol del usuario en la aplicación, no puede ser nulo.
        full_name (Column): Nombre completo del usuario, no puede ser nulo.
        phone_number (Column): Número de teléfono del usuario, no puede seer nulo.

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
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    cedula = Column(String, nullable=False, unique=True)
    credito = Column(Numeric(10, 2))

class Venta(Base):
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

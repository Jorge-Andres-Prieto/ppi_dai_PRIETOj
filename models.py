# Importa la función declarative_base de SQLAlchemy para la creación de modelos ORM
from sqlalchemy.ext.declarative import declarative_base
# Importa tipos de columnas específicos de SQLAlchemy para definir propiedades de modelo
from sqlalchemy import Column, Integer, String, Numeric

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
        phone_number (Column): Número de teléfono del usuario, no puede ser nulo.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

class Product(Base):
    """Define la estructura de la tabla 'products' para almacenar información de productos.

    Attributes:
        id (Column): Identificador único del producto, clave primaria.
        name (Column): Nombre del producto.
        brand (Column): Marca del producto.
        category (Column): Categoría del producto.
        subcategory (Column): Subcategoría del producto.
    """
    class Product(Base):
        __tablename__ = 'products'
        id = Column(Integer, primary_key=True)
        name = Column(String, nullable=False)
        brand = Column(String)
        category = Column(String, nullable=False)
        subcategory = Column(String)
        price = Column(Numeric(10, 2), nullable=False)
        quantity = Column(Integer, nullable=False)
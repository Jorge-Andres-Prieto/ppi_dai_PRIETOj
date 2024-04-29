# Importa la función declarative_base de SQLAlchemy para la creación de modelos ORM
from sqlalchemy.ext.declarative import declarative_base
# Importa tipos de columnas específicos de SQLAlchemy para definir propiedades de modelo
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship


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
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    user_data = relationship("UserData", uselist=False, back_populates="user", lazy='joined')


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    brand = Column(String)
    category = Column(String, nullable=False)
    subcategory = Column(String)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)


class UserData(Base):
    __tablename__ = 'user_data'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    inicio = Column(Integer, default=0)
    tdp = Column(String, default='No Aceptado')

    user = relationship("User", back_populates="user_data")
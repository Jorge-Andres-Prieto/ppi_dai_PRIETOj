# Importar la sesión de la base de datos
from database import Session

# Importar el modelo Cliente
from models import Cliente

# Importar operador lógico 'or' de SQLAlchemy
from sqlalchemy import or_

# Importar clase Decimal para manejo de números decimales
from decimal import Decimal


def create_client(nombre, direccion, telefono, cedula, credito):
    """
    Crea un nuevo cliente en la base de datos.

    Args:
        nombre (str): Nombre del cliente.
        direccion (str): Dirección del cliente.
        telefono (str): Teléfono del cliente.
        cedula (str): Cédula del cliente.
        credito (str): Crédito del cliente.

    Returns:
        str: Mensaje de éxito o error.
    """
    session = Session()
    try:
        new_client = Cliente(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            cedula=cedula,
            credito=credito
        )
        session.add(new_client)
        session.commit()
        return "Cliente creado con éxito."
    except Exception as e:
        session.rollback()
        return f"Error al crear el cliente: {str(e)}"
    finally:
        session.close()


def search_clients(query):
    """
    Busca clientes en la base de datos que coincidan con la consulta.

    Args:
        query (str): Cadena de búsqueda que puede coincidir con el nombre o cédula del cliente.

    Returns:
        list: Lista de clientes que coinciden con la consulta.
    """
    session = Session()
    try:
        clients = session.query(Cliente).filter(
            or_(
                Cliente.nombre.ilike(f"%{query}%"),
                Cliente.cedula.ilike(f"%{query}%")
            )
        ).all()
        return clients
    finally:
        session.close()


def update_client(cedula, new_nombre=None, new_direccion=None, new_telefono=None, new_credito=None):
    """
    Actualiza los datos de un cliente existente en la base de datos.

    Args:
        cedula (str): Cédula del cliente a actualizar.
        new_nombre (str, optional): Nuevo nombre del cliente. Defaults to None.
        new_direccion (str, optional): Nueva dirección del cliente. Defaults to None.
        new_telefono (str, optional): Nuevo teléfono del cliente. Defaults to None.
        new_credito (str, optional): Nuevo crédito del cliente. Defaults to None.

    Returns:
        str: Mensaje de éxito o error.
    """
    session = Session()
    try:
        client = session.query(Cliente).filter(Cliente.cedula == str(cedula)).first()  # Asegurarse de que cédula es una cadena
        if client:
            if new_nombre is not None:
                client.nombre = new_nombre
            if new_direccion is not None:
                client.direccion = new_direccion
            if new_telefono is not None:
                client.telefono = new_telefono
            if new_credito is not None:
                client.credito = Decimal(new_credito)
            session.commit()
            return "Cliente actualizado con éxito."
        else:
            return "Cliente no encontrado."
    except Exception as e:
        session.rollback()
        return f"Error al actualizar el cliente: {str(e)}"
    finally:
        session.close()


def update_client_credit(cedula, nuevo_credito):
    """
    Actualiza el crédito de un cliente en la base de datos.

    Args:
        cedula (str): Cédula del cliente a actualizar.
        nuevo_credito (str): Nuevo crédito del cliente.

    Returns:
        str: Mensaje de éxito o error.
    """
    session = Session()
    try:
        client = session.query(Cliente).filter(Cliente.cedula == str(cedula)).first()  # Asegurarse de que cédula es una cadena
        if client:
            client.credito = Decimal(nuevo_credito)
            session.commit()
            return "Crédito del cliente actualizado con éxito."
        else:
            return "Cliente no encontrado."
    except Exception as e:
        session.rollback()
        return f"Error al actualizar el crédito del cliente: {str(e)}"
    finally:
        session.close()


def delete_client(cedula):
    """
    Elimina un cliente de la base de datos.

    Args:
        cedula (str): Cédula del cliente a eliminar.

    Returns:
        str: Mensaje de éxito o error.
    """
    session = Session()
    try:
        client = session.query(Cliente).filter(Cliente.cedula == cedula).one_or_none()
        if client:
            session.delete(client)
            session.commit()
            return "Cliente eliminado con éxito."
        else:
            return "Cliente no encontrado."
    finally:
        session.close()


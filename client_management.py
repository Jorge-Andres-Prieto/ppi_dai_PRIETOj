from database import Session
from models import Cliente
from sqlalchemy import or_

def create_client(nombre, direccion, telefono, cedula, credito):
    session = Session()
    try:
        new_client = Cliente(nombre=nombre, direccion=direccion, telefono=telefono, cedula=cedula, credito=credito)
        session.add(new_client)
        session.commit()
        return "Cliente creado con éxito."
    except Exception as e:
        session.rollback()
        return f"Error al crear el cliente: {str(e)}"
    finally:
        session.close()

def search_clients(query):
    session = Session()
    try:
        clients = session.query(Cliente).filter(or_(Cliente.nombre.ilike(f"%{query}%"), Cliente.cedula.ilike(f"%{query}%"))).all()
        return clients
    finally:
        session.close()


def update_client_credit(client_id, new_credit):
    session = Session()
    try:
        client = session.query(Cliente).filter(Cliente.id == client_id).first()
        if client:
            client.credito = new_credit
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

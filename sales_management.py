from database import Session
from models import Venta, Product, Cliente
from datetime import datetime

def create_sale(user_id, total_efectivo, total_transferencia, productos_vendidos):
    session = Session()
    try:
        new_sale = Venta(user_id=user_id, total_efectivo=total_efectivo, total_transferencia=total_transferencia, productos_vendidos=productos_vendidos)
        session.add(new_sale)
        session.commit()
        return "Venta registrada con éxito."
    except Exception as e:
        session.rollback()
        return f"Error al registrar la venta: {str(e)}"
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

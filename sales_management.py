from database import Session
from models import Venta, Product, Cliente
from datetime import datetime

from datetime import datetime, timedelta

def obtener_hora_colombia():
    # Obtener la hora actual
    now = datetime.now()
    # Restar 5 horas para obtener la hora en la zona horaria de Colombia
    hora_colombia = now - timedelta(hours=5)
    return hora_colombia

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
        # Obtener la fecha y hora de Colombia restando 5 horas a la hora actual
        fecha_hora = obtener_hora_colombia()

        # Crear una nueva venta
        new_sale = Venta(
            user_id=user_id,
            fecha_hora=fecha_hora,
            total_efectivo=total_efectivo,
            total_transferencia=total_transferencia,
            total_credito=total_credito,
            productos_vendidos=[{
                'product_id': item['product'].product_id,
                'cantidad': item['quantity']
            } for item in productos_vendidos]
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

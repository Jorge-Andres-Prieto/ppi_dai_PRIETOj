from database import Session
from models import Venta, Product, Cliente
from datetime import datetime


def create_sale(user_id, total_efectivo, total_transferencia, productos_vendidos, total_credito, sitio):
    session = Session()
    try:
        productos_vendidos_str = ', '.join(
            [f"{item['product'].name} x {item['quantity']}" for item in productos_vendidos])
        new_sale = Venta(user_id=user_id, total_efectivo=total_efectivo, total_transferencia=total_transferencia,
                         productos_vendidos=productos_vendidos_str, total_credito=total_credito)
        session.add(new_sale)

        # Descontar la cantidad de productos vendidos del inventario en tienda
        for item in productos_vendidos:
            product = session.query(Product).filter(Product.product_id == item['product'].product_id).one_or_none()
            if product:
                if sitio == 'Tienda':
                    product.total_tienda -= item['quantity']

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

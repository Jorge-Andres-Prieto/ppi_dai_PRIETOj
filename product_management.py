''' Importa la clase Session del módulo database. Esta clase se utiliza para crear
    sesiones de interacción con la base de datos.'''
from database import Session

''' Importa la clase Product del módulo models. Esta clase representa
    el modelo de datos para los productos en la base de datos.'''
from models import Product

'''Importa funciones de la biblioteca sqlalchemy. La función func se 
   utiliza para crear expresiones SQL personalizadas.'''
from sqlalchemy import func


def search_products(search_query):
    """Busca productos que coincidan con un criterio de búsqueda en el nombre o ID.

    Args:
        search_query (str): Criterio de búsqueda.

    Returns:
        list: Lista de objetos Product que coinciden con la búsqueda.
    """
    session = Session()
    try:
        # Chequea si la entrada es numérica, asumiendo que es un ID
        if search_query.isdigit():
            product_id = int(search_query)
            products = session.query(Product).filter(Product.product_id == product_id).all()
        # De lo contrario, asume que es una búsqueda por nombre
        else:
            products = session.query(Product).filter(Product.name.ilike(f"%{search_query}%")).all()
        return products
    finally:
        session.close()


def view_product_details(product_id):
    """Obtiene y muestra la información detallada de un producto por su ID.

    Args:
        product_id (int): ID del producto a ver.

    Returns:
        None
    """
    session = Session()
    try:
        product = session.query(Product).filter(Product.id == product_id).first()
        if product:
            # Muestra la información detallada del producto
            print(f"ID: {product.id}, Nombre: {product.name}, Marca: {product.brand}, Categoría: {product.category}, Subcategoría: {product.subcategory}")
        else:
            print("Producto no encontrado.")
    finally:
        session.close()

def update_product(product_id, new_name=None, new_brand=None, new_category=None, new_subcategory=None, new_price=None, inventory_adjustment_tienda=None, inventory_adjustment_bodega=None):
    session = Session()
    try:
        product = session.query(Product).filter(Product.product_id == product_id).first()
        if product:
            if new_name:
                product.name = new_name
            if new_brand:
                product.brand = new_brand
            if new_category:
                product.category = new_category
            if new_subcategory:
                product.subcategory = new_subcategory
            if new_price is not None:
                product.price = new_price
            if inventory_adjustment_tienda is not None:
                product.total_tienda += inventory_adjustment_tienda
                if product.total_tienda < 0:
                    session.rollback()
                    return "La cantidad en tienda no puede ser negativa."
            if inventory_adjustment_bodega is not None:
                product.total_bodega += inventory_adjustment_bodega
                if product.total_bodega < 0:
                    session.rollback()
                    return "La cantidad en bodega no puede ser negativa."
            session.commit()
            return "Producto actualizado con éxito."
        else:
            return "Producto no encontrado."
    except Exception as e:
        session.rollback()
        return f"Error al actualizar el producto: {str(e)}"
    finally:
        session.close()

def add_product(product_id, name, brand, category, subcategory, price, cantidad):
    session = Session()
    try:
        new_product = Product(product_id=product_id, name=name, brand=brand, category=category, subcategory=subcategory, price=price, total_tienda=0, total_bodega=cantidad)
        session.add(new_product)
        session.commit()
        return "Producto añadido con éxito."
    except Exception as e:
        session.rollback()
        return f"Error al añadir el producto: {str(e)}"
    finally:
        session.close()



def delete_product(product_id):
    """Elimina un producto existente de la base de datos.

    Args:
        product_id (str): ID del producto a eliminar.

    Returns:
        str: Mensaje indicando si el producto fue eliminado o no.
    """
    session = Session()
    try:
        product = session.query(Product).filter(Product.product_id == product_id).one_or_none()
        if product:
            session.delete(product)
            session.commit()
            return "Producto eliminado con éxito."
        else:
            return "Producto no encontrado."
    except Exception as e:
        session.rollback()
        raise e  # Re-lanzar la excepción para que sea capturada en el formulario
    finally:
        session.close()

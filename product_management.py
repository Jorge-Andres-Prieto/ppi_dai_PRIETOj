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
    """Busca productos que coincidan con un criterio de búsqueda en el nombre.

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
            products = session.query(Product).filter(Product.id == product_id).all()
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

def update_product(product_id, new_name=None, new_brand=None, new_category=None, new_subcategory=None, new_price=None, sitio=None, inventory_adjustment=None):
    """Actualiza la información de un producto existente.

    Args:
        product_id (int): ID del producto a actualizar.
        new_name (str): Nuevo nombre del producto.
        new_brand (str): Nueva marca del producto.
        new_category (str): Nueva categoría del producto.
        new_subcategory (str): Nueva subcategoría del producto.
        new_price (float): Nuevo precio del producto.
        sitio (str): Nueva ubicación del producto (tienda o bodega).
        inventory_adjustment (int): Ajuste de inventario (positivo para añadir, negativo para reducir).

    Returns:
        str: Mensaje indicando si el producto fue actualizado o no.
    """
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
            if sitio:
                product.sitio = sitio
            if inventory_adjustment is not None:
                product.cantidad += inventory_adjustment
                if product.cantidad < 0:
                    session.rollback()  # Hacer rollback si la cantidad es negativa
                    return "La cantidad del producto no puede ser negativa."
            session.commit()
            return "Producto actualizado con éxito."
        else:
            return "Producto no encontrado."
    except Exception as e:
        session.rollback()
        return f"Error al actualizar el producto: {str(e)}"
    finally:
        session.close()



def add_product(product_id, name, brand, category, subcategory, price, sitio, cantidad):
    """Añade un nuevo producto a la base de datos.

    Args:
        product_id (str): Identificador del producto.
        name (str): Nombre del nuevo producto.
        brand (str): Marca del nuevo producto.
        category (str): Categoría del nuevo producto.
        subcategory (str): Subcategoría del nuevo producto.
        price (float): Precio del nuevo producto.
        sitio (str): Ubicación del producto (tienda o bodega).
        cantidad (int): Cantidad del nuevo producto.

    Returns:
        str: Mensaje indicando si el producto fue añadido o no.
    """
    session = Session()
    try:
        new_product = Product(product_id=product_id, name=name, brand=brand, category=category, subcategory=subcategory, price=price, sitio=sitio, cantidad=cantidad)
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
        None

    Returns:
        None
    """
    session = Session()
    try:
        product = session.query(Product).filter(Product.id == product_id).one_or_none()
        if product:
            session.delete(product)
            session.commit()
            return "Producto eliminado con éxito."
        else:
            return "Producto no encontrado."
    finally:
        session.close()
from database import Session
from models import Product
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
        if search_query.isdigit():  # Chequea si la entrada es numérica, asumiendo que es un ID
            product_id = int(search_query)
            products = session.query(Product).filter(Product.id == product_id).all()
        else:  # De lo contrario, asume que es una búsqueda por nombre
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

def update_product(product_id, new_name=None, new_brand=None, new_category=None, new_subcategory=None, new_price=None, inventory_adjustment=None):
    session = Session()
    """Actualiza la información de un producto existente.

    Args:
        product_id (int): ID del producto a actualizar.
        new_name (str): Nuevo nombre del producto.
        new_brand (str): Nueva marca del producto.
        new_category (str): Nueva categoría del producto.
        new_subcategory (str): Nueva subcategoría del producto.

    Returns:
        str: Mensaje indicando si el producto fue actualizado o no.
    """
    session = Session()
    try:
        product = session.query(Product).filter(Product.id == product_id).first()
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
            if inventory_adjustment != 0:
                product.quantity += inventory_adjustment
                if product.quantity < 0:
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

def add_product(name, brand, category, subcategory, price, quantity):
    """Añade un nuevo producto a la base de datos.

    Args:
        name (str): Nombre del nuevo producto.
        brand (str): Marca del nuevo producto.
        category (str): Categoría del nuevo producto.
        subcategory (str): Subcategoría del nuevo producto.

    Returns:
        str: Mensaje indicando si el producto fue añadido o no.
    """
    session = Session()
    try:
        new_product = Product(name=name, brand=brand, category=category, subcategory=subcategory, price=price,
                              quantity=quantity)
        session.add(new_product)
        session.commit()
        return "Producto añadido con éxito."
    except Exception as e:
        session.rollback()
        return f"Error al añadir el producto: {str(e)}"
    finally:
        session.close()

def delete_product(product_id):
    """Elimina un producto existente de la base de datos."""
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

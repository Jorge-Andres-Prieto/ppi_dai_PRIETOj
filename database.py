# Importa la función para crear motores de base de datos en SQLAlchemy
from sqlalchemy import create_engine

# Importa la función para crear fabricantes de sesiones en SQLAlchemy
from sqlalchemy.orm import sessionmaker

# Importa la clase Base desde los modelos para la definición de esquemas de la base de datos
from models import Base


# URL de conexión para la base de datos PostgreSQL alojada en Render
DATABASE_URL = (
    "postgresql://datos_usuarios_user:NNgnrDUS7HG3zQPuffAWnG3pyDvevRs2"
    "@dpg-coe966gl6cac73bvqv3g-a.oregon-postgres.render.com/datos_usuarios"
)

# Crea un motor SQLAlchemy que gestiona las conexiones a la base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crea una fábrica de sesiones de SQLAlchemy vinculada al motor
Session = sessionmaker(bind=engine)


def init_db():
    """
    Inicializa la base de datos creando todas las tablas definidas en los modelos.

    Args:
        None

    Returns:
        None
    """
    # Crea todas las tablas en la base de datos según lo definido en la clase Base
    Base.metadata.create_all(engine)

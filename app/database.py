import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session


# 1. direccion de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tareas.db")

# 2. Configuracion de la base de datos
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# 3. Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# 4. Crear la sesion de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Crear la clase base para los modelos
class Base(DeclarativeBase):
    pass


# 6.  dependencia de fastapi para obtener la sesion de la base de datos
def get_db():
    with SessionLocal() as session:
        yield session
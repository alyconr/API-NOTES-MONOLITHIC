from contextlib import asynccontextmanager


from fastapi import FastAPI

from sqlalchemy.engine import Engine


from app.api.tareas import router as tareas_router
from app.database import engine, Base

import app.models.tarea


def create_app(database_engine: Engine | None = None) -> FastAPI:

    selected_engine = database_engine or engine

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Crear las tablas en la base de datos al iniciar la aplicación
        Base.metadata.create_all(bind=selected_engine)
        yield
        # Aquí podrías agregar lógica para limpiar recursos al finalizar la aplicación si es necesario

    application = FastAPI(title="API de Tareas", version="1.0.0", lifespan=lifespan)

    # Agregar el router de tareas a la aplicación
    application.include_router(tareas_router, prefix="/api/v1", tags=["Tareas"])

    return application

app = create_app()
    

import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import get_db
from app.main import create_app


@pytest.fixture
def client():

    # Base de datos SQLite en memoria
    test_engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={
            "check_same_thread": False
        },
        poolclass=StaticPool
    )

    # Fábrica de sesiones de pruebas
    TestSessionLocal = sessionmaker(
        bind=test_engine,
        expire_on_commit=False
    )

    # Crear aplicación usando la base de pruebas
    test_app = create_app(
        database_engine=test_engine
    )

    # Sustituir la dependencia de BD
    def get_test_db():
        with TestSessionLocal() as session:
            yield session

    test_app.dependency_overrides[get_db] = get_test_db

    # Cliente HTTP de pruebas
    with TestClient(test_app) as test_client:
        yield test_client

    # Limpieza
    test_app.dependency_overrides.clear()
    test_engine.dispose()
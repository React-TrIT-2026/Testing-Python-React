import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient

from src.app import app, Base, get_db

@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite:///:memory:", # Memoria, no disco
        connect_args={"check_same_thread": False}, # Simplificamos las cosas para tests, no necesitamos concurrencia
        poolclass=StaticPool, # Volvemos StaticPool para que la conexión se mantenga viva durante todo el test, y no se cierre al salir del contexto
    )

    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback() # Rollback al terminar el test, para que cada test empiece con la BD limpia
        session.close()

@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
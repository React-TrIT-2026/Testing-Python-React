"""
API mínima de pedidos para la práctica de testing con FastAPI + TestClient.

Un solo archivo a propósito -- para una práctica de 40 minutos no hace
falta separar en capas. En un proyecto real, models/routes/db irían aparte.
"""

from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = "sqlite:///./pedidos.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class PedidoDB(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, nullable=False)
    total = Column(Float, nullable=False)
    estado = Column(String, default="pendiente")
    creado_en = Column(DateTime, default=datetime.utcnow)


class PedidoCrear(BaseModel):
    cliente: str
    total: float


class PedidoRespuesta(BaseModel):
    id: int
    cliente: str
    total: float
    estado: str

    class Config:
        from_attributes = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.post("/pedidos", response_model=PedidoRespuesta, status_code=201)
def crear_pedido(pedido: PedidoCrear, db: Session = Depends(get_db)):
    if pedido.total <= 0:
        raise HTTPException(status_code=400, detail="El total debe ser mayor que 0")
    nuevo = PedidoDB(cliente=pedido.cliente, total=pedido.total)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@app.get("/pedidos/{pedido_id}", response_model=PedidoRespuesta)
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(PedidoDB).filter(PedidoDB.id == pedido_id).first()
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


@app.post("/pedidos/{pedido_id}/confirmar", response_model=PedidoRespuesta)
def confirmar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(PedidoDB).filter(PedidoDB.id == pedido_id).first()
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if pedido.estado != "pendiente":
        raise HTTPException(status_code=400, detail=f"No se puede confirmar un pedido en estado '{pedido.estado}'")
    pedido.estado = "confirmado"
    db.commit()
    db.refresh(pedido)
    return pedido

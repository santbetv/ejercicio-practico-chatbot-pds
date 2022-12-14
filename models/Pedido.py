
import database.db as db
from sqlalchemy import Column, Identity, Integer, String, Float, BOOLEAN, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship


class Pedido(db.Base):
    __tablename__ = 'tbl_Pedidos'
    id = Column('idPedido', Integer, Identity(
        start=0, cycle=True), primary_key=True, nullable=False)
    direccion = Column('direccionPedido', String(100),
                       nullable=False)
    estado = Column('estadoPedido', String(100),
                    nullable=False)
    valorTotal = Column('valorTotalPedido', String(100),
                        nullable=False)
    IdPersona = Column('idPersona', Integer, ForeignKey(
        'tbl_Personas.idPersona', onupdate='CASCADE'), nullable=False)
    fechaCreacion = Column('fechaCreacionItemCategoria', DateTime(
        timezone=True), server_default=func.now())
    Personas = relationship("Persona", back_populates="Pedidos")
    ItemsCategoriaPedido = relationship(
        "ItemsCategoriaPedido", back_populates="Pedidos")

    def __init__(self, direccion, estado, valorTotal, idPersona):
        self.direccion = direccion
        self.estado = estado
        self.valorTotal = valorTotal
        self.IdPersona = idPersona

    def __repr__(self):
        return f"<Pedido {self.id}>"


import database.db as db
from sqlalchemy import Column, Identity, Integer, String, Float, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship


class ItemsCategoriaPedido(db.Base):
    __tablename__ = 'tbl_ItemsCategoriaPedidos'
    id = Column('idItemCategoriaPedido', Integer, Identity(
        start=0, cycle=True), primary_key=True, nullable=False)
    idPedido = Column('idPedido', String(15), ForeignKey(
        'tbl_Pedidos.idPedido', onupdate='CASCADE'),
        nullable=False)
    idItemCategoria = Column('idItemCategoria', Integer, ForeignKey(
        'tbl_ItemsCategoria.idItemCategoria', onupdate='CASCADE'), nullable=False)

    Pedidos = relationship(
        "Pedido", back_populates="ItemsCategoriaPedido")
    ItemCategoria = relationship(
        "ItemCategoria", back_populates="ItemsCategoriaPedido")

    def __init__(self, idPedido,  idItemCategoria):
        self.idPedido = idPedido        
        self.idItemCategoria = idItemCategoria

    def __repr__(self):
        return f"<itemCategoriaPedido {self.id}>"

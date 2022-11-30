
import database.db as db
from sqlalchemy import Column, Integer, String, Float, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship


class ItemsCategoriaPedido(db.Base):
    __tablename__ = 'tbl_ItemsCategoriaPedidos'
    id = Column('idItemCategoriaPedido', String(15),
                primary_key=True, nullable=False)
    idPedido = Column('idPedido', String(15), ForeignKey(
        'tbl_Pedidos.idPedido', onupdate='CASCADE'),
        nullable=False)
    idItemCategoria = Column('idItemCategoria', String(15), ForeignKey(
        'tbl_ItemsCategoria.idItemCategoria', onupdate='CASCADE'), nullable=False)

    Pedidos = relationship(
        "Pedido", back_populates="ItemsCategoriaPedido")
    ItemCategoria = relationship(
        "ItemCategoria", back_populates="ItemsCategoriaPedido")

    def __init__(self, id, idPedido,  idItemCategoria):
        self.id = id
        self.idPedido = idPedido        
        self.idItemCategoria = idItemCategoria

    def __repr__(self):
        return f"<itemCategoriaPedido {self.id}>"

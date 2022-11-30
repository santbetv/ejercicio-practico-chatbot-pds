
import database.db as db
from sqlalchemy import Column, Integer, String, Float, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship


class ItemCategoria(db.Base):
    __tablename__ = 'tbl_ItemsCategoria'
    id = Column('idItemCategoria', String(15),
                primary_key=True, nullable=False)
    descripcion = Column('descripcionItemCategoria',  String(50),
                         server_default='0', nullable=False)
    estado = Column('estadoItemCategoria', BOOLEAN,
                    server_default='1', nullable=False)
    idItemCategoria = Column('idCategoria', String(15), ForeignKey(
        'tbl_Categorias.idCategoria', onupdate='CASCADE'), nullable=False)
    
    Categoria = relationship("Categoria", back_populates="ItemCategoria")

    ItemsCategoriaPedido = relationship(
        "ItemsCategoriaPedido", back_populates="ItemCategoria")

    def __init__(self, id, descripcion, estado, idItemCategoria):
        self.id = id
        self.descripcion = descripcion
        self.estado = estado
        self.idItemCategoria = idItemCategoria

    def __repr__(self):
        return f"<ItemCategoria {self.id}>"

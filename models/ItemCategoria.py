
import database.db as db
from sqlalchemy import Column, DateTime, Identity, Integer, String, Float, BOOLEAN, ForeignKey, func
from sqlalchemy.orm import relationship


class ItemCategoria(db.Base):
    __tablename__ = 'tbl_ItemsCategoria'
    id = Column('idItemCategoria', Integer, Identity(
        start=0, cycle=True), primary_key=True, nullable=False)
    nombre = Column('nombreItemCategoria',  String(50),
                    server_default='0', nullable=False)
    descripcion = Column('descripcionItemCategoria',  String(50),
                         server_default='0', nullable=False)
    estado = Column('estadoItemCategoria', BOOLEAN,
                    server_default='1', nullable=False)
    precio = Column('precioItemCategoria', Integer,
                    server_default='1', nullable=False)
    fechaCreacion = Column('fechaCreacionItemCategoria', DateTime(
        timezone=True), server_default=func.now())
    idItemCategoria = Column('idCategoria', Integer, ForeignKey(
        'tbl_Categorias.idCategoria', onupdate='CASCADE'), nullable=False)

    Categoria = relationship("Categoria", back_populates="ItemCategoria")

    ItemsCategoriaPedido = relationship(
        "ItemsCategoriaPedido", back_populates="ItemCategoria")

    def __init__(self):
        pass

    def __init__(self,  nombre, descripcion, precio, idItemCategoria):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.idItemCategoria = idItemCategoria

    def __repr__(self):
        return f"<ItemCategoria {self.id}>"

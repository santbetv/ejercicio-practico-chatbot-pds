import database.db as db
from sqlalchemy import Column, Identity, Integer, String, Float, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship


class Categoria(db.Base):
    __tablename__ = 'tbl_Categorias'
    id = Column('idCategoria', Integer, Identity(
        start=0, cycle=True), primary_key=True, nullable=False)
    descripcion = Column('descripcionCategoria', String(50),
                         server_default='0', nullable=False)
    estado = Column('estadoCategoria', BOOLEAN,
                    server_default='1', nullable=False)
    idMenuCategoria = Column('idMenuCategoria', Integer, ForeignKey(
        'tbl_Menus.idMenu', onupdate='CASCADE'), nullable=False)

    Menu = relationship("Menu", back_populates="Categoria")

    ItemCategoria = relationship("ItemCategoria", back_populates="Categoria")

    def __init__(self, descripcion,  idMenuCategoria, estado=True):
        self.descripcion = descripcion
        self.idMenuCategoria = idMenuCategoria
        self.estado = estado

    def __repr__(self):
        return f"<Categoria {self.id}, {self.descripcion}>"

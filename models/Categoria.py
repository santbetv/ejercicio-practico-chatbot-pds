import database.db as db
from sqlalchemy import Column, Integer, String, Float, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship


class Categoria(db.Base):
    __tablename__ = 'tbl_Categorias'
    id = Column('idCategoria', String(15), primary_key=True, nullable=False)
    descripcion = Column('descripcionCategoria', String(50),
                         server_default='0', nullable=False)
    estado = Column('estadoCategoria', BOOLEAN,
                    server_default='1', nullable=False)
    idMenuCategoria = Column('idMenuCategoria', String(15), ForeignKey(
        'tbl_Menus.idMenu', onupdate='CASCADE'), nullable=False)

    Menu = relationship("Menu", back_populates="Categoria")
    
    ItemCategoria = relationship("ItemCategoria", back_populates="Categoria")
    
    def __init__(self, id, descripcion, estado, idMenuCategoria):
        self.id = id
        self.descripcion = descripcion
        self.estado = estado
        self.idMenuCategoria = idMenuCategoria

    def __repr__(self):
        return f"<Categoria {self.id}, {self.descripcion}>"

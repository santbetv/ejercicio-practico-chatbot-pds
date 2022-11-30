import database.db as db
from sqlalchemy import Column, Integer, String, Float, BOOLEAN
from sqlalchemy.orm import relationship


class Menu(db.Base):
    __tablename__ = 'tbl_Menus'
    id = Column('idMenu', String(15), primary_key=True, nullable=False)
    descripcion = Column('descripcionMenu', String(
        50), server_default='0', nullable=False)
    estado = Column('estadoMenu',  String(
        50), server_default='1', nullable=False)

    Categoria = relationship("Categoria", back_populates="Menu")

    def __init__(self, id, descripcion, estado):
        self.id = id
        self.descripcion = descripcion
        self.estado = estado

    def __repr__(self):
        return f"<Menu {self.id}, {self.descripcion}>"

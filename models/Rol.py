
import database.db as db
from sqlalchemy import Column, Identity, Integer, String, Float, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship


class Rol(db.Base):
    __tablename__ = 'tbl_Roles'
    id = Column('idRol', Integer, Identity(
        start=0, cycle=True), primary_key=True, nullable=False)
    nombre = Column('NombreRol', String(100),
                    nullable=False)
    Personas = relationship("Persona", back_populates="Roles")

    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

    def __repr__(self):
        return f"<Rol {self.id}>"

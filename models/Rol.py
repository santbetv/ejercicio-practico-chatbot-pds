
import database.db as db
from sqlalchemy import Column, Integer, String, Float, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship


class Rol(db.Base):
    __tablename__ = 'tbl_Roles'
    id = Column('idRol', String(15),
                primary_key=True, nullable=False)
    nombre = Column('NombreRol', String(100),
                    nullable=False)
    Personas = relationship("Persona", back_populates="Roles")

    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

    def __repr__(self):
        return f"<Rol {self.id}>"

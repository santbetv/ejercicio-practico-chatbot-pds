import database.db as db
from sqlalchemy import Column, Integer, String, Float, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship


class Persona(db.Base):
    __tablename__ = 'tbl_Personas'
    id = Column('idPersona', String(15), primary_key=True, nullable=False)
    nombre = Column('nombrePersona', String(15), nullable=False)
    apellido = Column('apellidoPersona', String(
        15), nullable=False)
    direccion = Column('direccionPersona', String(
        15), nullable=False)
    telefono = Column('telefonoPersona', String(
        15), nullable=False)
    barrio = Column('barrioPersona', String(
        20), nullable=False)
    idRol = Column('idRol', String(15), ForeignKey(
        'tbl_Roles.idRol', onupdate='CASCADE'), nullable=False)
    Pedidos = relationship("Pedido", back_populates="Personas")

    Roles = relationship("Rol", back_populates="Personas")

    def __init__(self, id, nombre, apellido, direccion, telefono, barrio, idRol):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.telefono = telefono
        self.barrio = barrio
        self.idRol = idRol

    def __repr__(self):
        return f"<Persona {self.id}, {self.nombre}>"

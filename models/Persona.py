import database.db as db
from sqlalchemy import Column, Identity, Integer, String, Float, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship


class Persona(db.Base):
    __tablename__ = 'tbl_Personas'
    id = Column('idPersona', Integer, Identity(
        start=0, cycle=True), primary_key=True, nullable=False)
    cedula = Column('cedulaPersona', String(20), nullable=False)
    nombre = Column('nombrePersona', String(50), nullable=False)    
    direccion = Column('direccionPersona', String(
        50), nullable=False)
    telefono = Column('telefonoPersona', String(
        15), nullable=False)    
    idRol = Column('idRol', Integer, ForeignKey(
        'tbl_Roles.idRol', onupdate='CASCADE'), nullable=False)
    Pedidos = relationship("Pedido", back_populates="Personas")

    Roles = relationship("Rol", back_populates="Personas")

    def __init__(self, cedula, nombre,  direccion, telefono, idRol=2):
        self.cedula=cedula
        self.nombre = nombre        
        self.direccion = direccion
        self.telefono = telefono        
        self.idRol = idRol

    def __repr__(self):
        return f"<Persona {self.id}, {self.nombre}>"

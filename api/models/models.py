from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from api.db import engine

Base = declarative_base()

class Categorias(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True)
    titulo = Column(String(255), nullable=False)

class Nominados(Base):
    __tablename__ = "nominados"
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(255), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False) 
    representacion = Column(Text, nullable=True) 

class Votaciones(Base):
    __tablename__ = "votaciones"

    id = Column(Integer, primary_key=True)
    nombre_elector = Column(String(255), nullable=False)
    nominado_id = Column(Integer, ForeignKey("nominados.id"), nullable=False)
    voto_valido = Column(Boolean, default=True)

Base.metadata.create_all(engine)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api.models.models import Categorias, Nominados, Votaciones, Patrocinadores
from api.db import session

import sys
import os
from typing import List

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Modelo de entrada para validar la solicitud
class VotacionCreate(BaseModel):
    nombre_elector: str
    nominados: List[int]  # Lista de nominados_id

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen (en producción, especifica dominios permitidos)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)

@app.get("/categorias/")
def obtener_categorias():
    categorias = session.query(Categorias).order_by(Categorias.id).all()
    return {
        "categorias": [
            {
                "id": categoria.id, 
                "titulo": categoria.titulo
            } 
        for categoria in categorias]
    }

@app.get("/nominados/")
def obtener_nominados():
    nominados = session.query(Nominados).order_by(Nominados.id).all()
    return {
        "nominados": [
            {
                "id": nominado.id, 
                "descripcion": nominado.descripcion, 
                "representacion": nominado.representacion,
                "categoria": nominado.categoria_id
            } 
        for nominado in nominados]
    }

@app.get("/nominados_de_categoria_{categoria_id}/")
def obtener_nominados_por_categoria(categoria_id: int):
    nominados = session.query(Nominados).filter(Nominados.categoria_id == categoria_id).order_by(Nominados.id).all()
    return {
        "nominados": [
            {
                "id": nominado.id, 
                "descripcion": nominado.descripcion, 
                "representacion": nominado.representacion,
                "categoria": nominado.categoria_id
            } 
        for nominado in nominados]
    }

@app.get("/patrocinadores/")
def obtener_patrocinadores():
    patrocinadores = session.query(Patrocinadores).order_by(Patrocinadores.id).all()
    return {
        "nominados": [
            {
                "id": patrocinador.id, 
                "nombre": patrocinador.nombre, 
                "representacion": patrocinador.representacion
            } 
        for patrocinador in patrocinadores]
    }

@app.post("/votaciones/")
def crear_votacion(votacion: VotacionCreate):
    try:
        # Crear una votación para cada nominado_id en la lista
        for nominado_id in votacion.nominados:
            nueva_votacion = Votaciones(
                nombre_elector=votacion.nombre_elector,
                nominado_id=nominado_id,
            )
            session.add(nueva_votacion)
        
        # Confirmar los cambios en la base de datos
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar las votaciones: {str(e)}")

    return {"message": "Votaciones creadas con éxito"}

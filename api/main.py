from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api.models.models import Categorias, Nominados, Votaciones, Patrocinadores
from api.db import session

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Modelo de entrada para validar la solicitud
class VotacionCreate(BaseModel):
    nombre_elector: str
    nominado_id: int
    voto_valido: bool = True

app = FastAPI()

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

@app.post("/votaciones/")
def crear_votacion(votacion: VotacionCreate):
    nueva_votacion = Votaciones(
        nombre_elector=votacion.nombre_elector,
        nominado_id=votacion.nominado_id,
        voto_valido=votacion.voto_valido
    )

    try:
        session.add(nueva_votacion)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar la votación: {str(e)}")

    return {"message": "Votación creada con éxito", "id": nueva_votacion.id}

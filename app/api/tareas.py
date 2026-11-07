from typing import Annotated

from fastapi import ( APIRouter, Depends, HTTPException, status, Path)

from sqlalchemy.orm import Session

from app.database import get_db
from app.services.tarea_service import TareaService, TareaNoEncontradaError
from app.repositories.tarea_repository import TareaRepository
from app.schemas.tarea import TareaCrear, TareaRespuesta



#Endpoint router
router = APIRouter(
    prefix="/tareas",
    tags=["Tareas"],
)


#ENDPOINT DE ESCRITURA

@router.post("/", response_model=TareaRespuesta, status_code=status.HTTP_201_CREATED)
def crear_tarea(tarea_crear: TareaCrear, db: Annotated[Session, Depends(get_db)]):
    tarea_service = TareaService(TareaRepository(db))
    return tarea_service.crear_tarea(tarea_crear)

#ENDPOINT DE LECTURA

@router.get("/", response_model=list[TareaRespuesta])
def obtener_tareas(db: Annotated[Session, Depends(get_db)]):
    tarea_service = TareaService(TareaRepository(db))
    return tarea_service.obtener_tareas()

@router.get("/{tarea_id}", response_model=TareaRespuesta)
def obtener_tarea_por_id(tarea_id: Annotated[int, Path(gt=0)], db: Annotated[Session, Depends(get_db)]):
    tarea_service = TareaService(TareaRepository(db))
    try:
        return tarea_service.obtener_tarea_por_id(tarea_id)
    except TareaNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

#ENDPOINT DE ACTUALIZACION

@router.put("/{tarea_id}", response_model=TareaRespuesta)
def actualizar_tarea(tarea_id: Annotated[int, Path(gt=0)], tarea_actualizar: TareaCrear, db: Annotated[Session, Depends(get_db)]):
    tarea_service = TareaService(TareaRepository(db))
    try:
        return tarea_service.actualizar_tarea(tarea_id, tarea_actualizar)
    except TareaNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

#ENDPOINT DE ELIMINACION

@router.delete("/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tarea(tarea_id: Annotated[int, Path(gt=0)], db: Annotated[Session, Depends(get_db)]):
    tarea_service = TareaService(TareaRepository(db))
    try:
        tarea_service.eliminar_tarea(tarea_id)
    except TareaNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    


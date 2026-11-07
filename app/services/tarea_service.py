from app.models.tarea import Tarea
from app.repositories.tarea_repository import TareaRepository
from app.schemas.tarea import TareaCrear, TareaRespuesta


class TareaNoEncontradaError(Exception):
    pass


class TareaService:
    def __init__(self, tarea_repository: TareaRepository):
        self.tarea_repository = tarea_repository

    def crear_tarea(self, tarea_crear: TareaCrear) -> TareaRespuesta:
        nueva_tarea = Tarea(
            titulo=tarea_crear.titulo,
            descripcion=tarea_crear.descripcion,
            completada=tarea_crear.completada
        )
        tarea_creada = self.tarea_repository.crear_tarea(nueva_tarea)
        return TareaRespuesta.from_orm(tarea_creada)

    def obtener_tareas(self) -> list[TareaRespuesta]:
        tareas = self.tarea_repository.obtener_tareas()
        return [TareaRespuesta.from_orm(tarea) for tarea in tareas]

    def obtener_tarea_por_id(self, tarea_id: int) -> TareaRespuesta:
        tarea = self.tarea_repository.obtener_tarea_por_id(tarea_id)
        if not tarea:
            raise TareaNoEncontradaError(f"Tarea con ID {tarea_id} no encontrada.")
        return TareaRespuesta.from_orm(tarea)

    def actualizar_tarea(self, tarea_id: int, tarea_actualizar: TareaCrear) -> TareaRespuesta:
        tarea_existente = self.tarea_repository.obtener_tarea_por_id(tarea_id)
        if not tarea_existente:
            raise TareaNoEncontradaError(f"Tarea con ID {tarea_id} no encontrada.")

        tarea_existente.titulo = tarea_actualizar.titulo
        tarea_existente.descripcion = tarea_actualizar.descripcion
        tarea_existente.completada = tarea_actualizar.completada

        tarea_actualizada = self.tarea_repository.actualizar_tarea(tarea_existente)
        return TareaRespuesta.from_orm(tarea_actualizada)

    def eliminar_tarea(self, tarea_id: int) -> None:
        tarea_existente = self.tarea_repository.obtener_tarea_por_id(tarea_id)
        if not tarea_existente:
            raise TareaNoEncontradaError(f"Tarea con ID {tarea_id} no encontrada.")

        self.tarea_repository.eliminar_tarea(tarea_existente)

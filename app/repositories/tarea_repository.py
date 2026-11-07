from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.tarea import Tarea



class TareaRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear_tarea(self, tarea: Tarea) -> Tarea:
        try:
            self.db.add(tarea)
            self.db.commit()
            self.db.refresh(tarea)
            return tarea
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def obtener_tareas(self) -> list[Tarea]:
        return self.db.query(Tarea).all()

    def obtener_tarea_por_id(self, tarea_id: int) -> Tarea | None:
        return self.db.query(Tarea).filter(Tarea.id == tarea_id).first()

    def actualizar_tarea(self, tarea: Tarea) -> Tarea:
        try:
            self.db.commit()
            self.db.refresh(tarea)
            return tarea
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def eliminar_tarea(self, tarea: Tarea) -> None:
        try:
            self.db.delete(tarea)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
from sqlalchemy import String 
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Tarea(Base):
    __tablename__ = "tareas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    completada: Mapped[bool] = mapped_column(nullable=False, default=False)
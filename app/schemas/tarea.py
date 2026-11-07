from pydantic import BaseModel, ConfigDict, Field

#contrato de entrada para crear una tarea POST

class TareaCrear(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    titulo: str = Field(max_length=100, min_length=3)
    descripcion: str | None = Field(default=None, max_length=255)
    completada: bool = Field(default=False)  

# contrato de salida para mostrar una tarea GET
class TareaRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    titulo: str
    descripcion: str | None
    completada: bool


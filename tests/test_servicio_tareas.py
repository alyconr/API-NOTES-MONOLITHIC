from unittest.mock import Mock

import pytest

from app.models.tarea import Tarea
from app.repositories.tarea_repository import TareaRepository
from app.schemas.tarea import TareaCrear
from app.services.tarea_service import TareaNoEncontradaError, TareaService


def test_servicio_crea_tarea_sin_completar():
    repositorio = Mock(spec=TareaRepository)

    # Simular la BD: guardar la tarea le asigna un id
    def simular_guardado(tarea):
        tarea.id = 1
        return tarea

    repositorio.crear_tarea.side_effect = simular_guardado

    servicio = TareaService(repositorio)
    tarea = servicio.crear_tarea(TareaCrear(titulo="Preparar revisión"))

    assert tarea.id == 1
    assert tarea.completada is False

    repositorio.crear_tarea.assert_called_once()
    assert isinstance(repositorio.crear_tarea.call_args.args[0], Tarea)


def test_servicio_informa_cuando_no_existe():
    repositorio = Mock(spec=TareaRepository)
    repositorio.obtener_tarea_por_id.return_value = None

    servicio = TareaService(repositorio)

    with pytest.raises(TareaNoEncontradaError):
        servicio.obtener_tarea_por_id(42)

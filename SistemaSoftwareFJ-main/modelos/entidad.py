from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):
    """
    Clase abstracta base para todas las entidades del sistema.
    """

    def __init__(self, identificador):
        if identificador is None or (isinstance(identificador, str) and not identificador.strip()):
            raise ValueError("El identificador de la entidad no puede ser None ni estar vacío.")

        self._id = identificador
        self._fecha_creacion = datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @abstractmethod
    def mostrar_info(self):
        pass
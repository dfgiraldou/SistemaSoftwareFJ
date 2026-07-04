from abc import ABC, abstractmethod
from functools import total_ordering
from modelos.entidad import Entidad
from excepciones.excepciones import ServicioError


@total_ordering
class Servicio(Entidad, ABC):
    """
    Clase abstracta que representa un servicio general.
    Toda subclase de Servicio hereda automáticamente la comparación
    por costo_base (==, <, <=, >, >=) gracias a @total_ordering.
    """

    def __init__(self, identificador, nombre, costo_base):
        super().__init__(identificador)

        if not nombre or not nombre.strip():
            raise ServicioError("El nombre del servicio no puede estar vacío.")

        if not isinstance(costo_base, (int, float)) or isinstance(costo_base, bool):
            raise ServicioError("El costo base debe ser un valor numérico.")

        if costo_base <= 0:
            raise ServicioError("El costo del servicio debe ser mayor que cero.")

        self._nombre = nombre.strip()
        self._costo_base = costo_base

    @property
    def nombre(self):
        return self._nombre

    @property
    def costo_base(self):
        return self._costo_base

    @abstractmethod
    def calcular_costo(self):
        """Cada servicio especializado define su propia fórmula de costo."""
        pass

    @abstractmethod
    def describir(self):
        """Cada servicio especializado describe su naturaleza particular."""
        pass

    def mostrar_info(self):
        return (
            f"Servicio: {self._nombre}\n"
            f"Costo Base: ${self._costo_base:,.2f}"
        )

    # --- Comparación por costo_base (elimina el monkey-patch de la GUI) ---
    def _obtener_valor_comparable(self, otro):
        if isinstance(otro, Servicio):
            return otro._costo_base
        if isinstance(otro, (int, float)):
            return otro
        return None

    def __eq__(self, otro):
        valor = self._obtener_valor_comparable(otro)
        if valor is None:
            return NotImplemented
        return self._costo_base == valor

    def __lt__(self, otro):
        valor = self._obtener_valor_comparable(otro)
        if valor is None:
            return NotImplemented
        return self._costo_base < valor

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return self.mostrar_info()

    def __repr__(self):
        return f"{self.__class__.__name__}(nombre={self._nombre!r}, costo_base={self._costo_base})"
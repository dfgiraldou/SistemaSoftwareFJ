from modelos.servicio import Servicio
from excepciones.excepciones import ServicioError


class AlquilerEquipo(Servicio):
    """
    Servicio de alquiler de equipos.
    """

    def __init__(self, identificador, nombre, costo_base, tipo_equipo):
        super().__init__(identificador, nombre, costo_base)

        if not tipo_equipo or not tipo_equipo.strip():
            raise ServicioError("El tipo de equipo no puede estar vacío.")

        self._tipo_equipo = tipo_equipo.strip()

    @property
    def tipo_equipo(self):
        return self._tipo_equipo

    def calcular_costo(self, dias=1, descuento=0, impuesto=0):
        if not isinstance(dias, (int, float)) or dias <= 0:
            raise ServicioError("Los días deben ser un número mayor que cero.")

        if descuento < 0:
            raise ServicioError("El descuento no puede ser negativo.")

        if impuesto < 0:
            raise ServicioError("El impuesto no puede ser negativo.")

        subtotal = self.costo_base * dias

        if descuento > subtotal:
            raise ServicioError(
                "El descuento no puede ser mayor que el subtotal del servicio."
            )

        subtotal -= descuento
        total = subtotal + (subtotal * impuesto / 100)
        return round(total, 2)

    def describir(self):
        return f"Alquiler de equipo tipo {self._tipo_equipo}"

    def mostrar_info(self):
        return (
            f"{super().mostrar_info()}\n"
            f"Equipo: {self._tipo_equipo}"
        )
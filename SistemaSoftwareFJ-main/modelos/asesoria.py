from modelos.servicio import Servicio
from excepciones.excepciones import ServicioError


class Asesoria(Servicio):
    """
    Servicio de asesoría especializada.
    """

    def __init__(self, identificador, nombre, costo_base, especialidad):
        super().__init__(identificador, nombre, costo_base)

        if not especialidad or not especialidad.strip():
            raise ServicioError("La especialidad no puede estar vacía.")

        self._especialidad = especialidad.strip()

    @property
    def especialidad(self):
        return self._especialidad

    def calcular_costo(self, horas=1, descuento=0, impuesto=0):
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ServicioError("Las horas deben ser un número mayor que cero.")

        if descuento < 0:
            raise ServicioError("El descuento no puede ser negativo.")

        if impuesto < 0:
            raise ServicioError("El impuesto no puede ser negativo.")

        subtotal = self.costo_base * horas

        if descuento > subtotal:
            raise ServicioError(
                "El descuento no puede ser mayor que el subtotal del servicio."
            )

        subtotal -= descuento
        total = subtotal + (subtotal * impuesto / 100)
        return round(total, 2)

    def describir(self):
        return f"Asesoría especializada en {self._especialidad}"

    def mostrar_info(self):
        return (
            f"{super().mostrar_info()}\n"
            f"Especialidad: {self._especialidad}"
        )
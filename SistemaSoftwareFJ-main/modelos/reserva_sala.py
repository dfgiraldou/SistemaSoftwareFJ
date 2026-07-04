from modelos.servicio import Servicio
from excepciones.excepciones import ServicioError


class ReservaSala(Servicio):
    """
    Servicio de reserva de salas.
    Es un tipo de Servicio (junto con AlquilerEquipo y Asesoria),
    NO un tipo de Reserva. Un cliente que quiera una sala primero
    selecciona/crea este servicio, y luego se vincula a través de
    una Reserva normal (ver modelos/reserva.py).
    """

    def __init__(self, identificador, nombre, costo_base, capacidad):
        super().__init__(identificador, nombre, costo_base)

        if not isinstance(capacidad, (int, float)) or isinstance(capacidad, bool) or capacidad <= 0:
            raise ServicioError("La capacidad debe ser un número mayor que cero.")

        self._capacidad = capacidad

    @property
    def capacidad(self):
        return self._capacidad

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
        return f"Reserva de sala para {self._capacidad} personas."

    def mostrar_info(self):
        return (
            f"{super().mostrar_info()}\n"
            f"Capacidad: {self._capacidad}"
        )
from modelos.entidad import Entidad
from modelos.cliente import Cliente
from modelos.servicio import Servicio
from excepciones.excepciones import ReservaError, OperacionError


class Reserva(Entidad):
    """
    Clase que representa una reserva de un servicio.
    Vincula un Cliente con un Servicio (sin importar cuál de las
    tres especializaciones sea: AlquilerEquipo, Asesoria o ReservaSala).
    """

    def __init__(self, identificador, cliente, servicio, duracion):
        super().__init__(identificador)

        if not isinstance(cliente, Cliente):
            raise ReservaError("El cliente proporcionado no es válido.")

        if not isinstance(servicio, Servicio):
            raise ReservaError("El servicio proporcionado no es válido.")

        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise ReservaError("La duración debe ser un número mayor que cero.")

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    def confirmar(self):
        """
        Confirma la reserva.
        """
        if self.__estado == "Cancelada":
            raise OperacionError("No se puede confirmar una reserva cancelada.")

        if self.__estado == "Confirmada":
            raise OperacionError("La reserva ya se encuentra confirmada.")

        self.__estado = "Confirmada"

    def cancelar(self):
        """
        Cancela la reserva.
        """
        if self.__estado == "Cancelada":
            raise OperacionError("La reserva ya fue cancelada.")

        self.__estado = "Cancelada"

    def procesar(self):
        """
        Procesa la reserva y calcula el costo.
        """
        try:
            costo = self.__servicio.calcular_costo(self.__duracion)

        except Exception as error:
            raise ReservaError("Error al procesar la reserva.") from error

        else:
            return costo

        finally:
            print("Proceso de reserva finalizado.")

    def mostrar_info(self):
        """
        Muestra la información de la reserva.
        """
        return (
            f"ID Reserva: {self.id}\n"
            f"Cliente: {self.__cliente.nombre}\n"
            f"Servicio: {self.__servicio.nombre}\n"
            f"Duración: {self.__duracion}\n"
            f"Estado: {self.__estado}"
        )
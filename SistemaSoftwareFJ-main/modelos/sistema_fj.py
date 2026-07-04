from logs.config_log import registrar_info, registrar_error
from excepciones.excepciones import ValidacionError, OperacionError


class SistemaFJ:
    """
    Clase que administra clientes, servicios y reservas.
    Es el único punto de entrada para modificar las listas internas:
    nadie debe acceder o mutar las listas directamente desde fuera.
    """

    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []

    # --- Generadores de ID consistentes ---
    def generar_id_cliente(self):
        return len(self._clientes) + 1

    def generar_id_servicio(self):
        return len(self._servicios) + 1

    def generar_id_reserva(self):
        return len(self._reservas) + 1

    # --- Registro de entidades ---
    def agregar_cliente(self, cliente):
        try:
            for c in self._clientes:
                if c.documento == cliente.documento:
                    raise ValidacionError("Ya existe un cliente con ese documento.")

        except ValidacionError as error:
            registrar_error(str(error))
            raise

        else:
            self._clientes.append(cliente)
            registrar_info(f"Cliente agregado: {cliente.nombre}")

    def agregar_servicio(self, servicio):
        try:
            for s in self._servicios:
                if s.nombre == servicio.nombre:
                    raise ValidacionError("Ya existe un servicio con ese nombre.")

        except ValidacionError as error:
            registrar_error(str(error))
            raise

        else:
            self._servicios.append(servicio)
            registrar_info(f"Servicio agregado: {servicio.nombre}")

    def agregar_reserva(self, reserva):
        try:
            if reserva is None:
                raise OperacionError("La reserva no puede ser nula.")

        except OperacionError as error:
            registrar_error(str(error))
            raise

        else:
            self._reservas.append(reserva)
            registrar_info("Reserva agregada correctamente.")

        finally:
            registrar_info("Proceso de registro de reserva finalizado.")

    # --- Acceso de solo lectura ---
    def listar_clientes(self):
        return list(self._clientes)

    def listar_servicios(self):
        return list(self._servicios)

    def listar_reservas(self):
        return list(self._reservas)
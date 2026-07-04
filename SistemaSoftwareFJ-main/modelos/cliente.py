from modelos.entidad import Entidad
from excepciones.excepciones import ValidacionError
from logs.config_log import registrar_info, registrar_error


class Cliente(Entidad):
    """
    Clase que representa un cliente del sistema.
    """

    def __init__(self, identificador, nombre, documento, correo, telefono):
        super().__init__(identificador)

        # Usamos .strip() desde la asignación para eliminar espacios accidentales al inicio/final
        self.__nombre = nombre.strip() if nombre else ""
        self.__documento = documento.strip() if documento else ""
        self.__correo = correo.strip() if correo else ""
        self.__telefono = telefono.strip() if telefono else ""

        self.validar_datos()

    def validar_datos(self):
        # 1. Validar que ningún campo esencial esté completamente vacío
        if not self.__nombre:
            registrar_error("Nombre de cliente vacío.")
            raise ValidacionError("El nombre no puede estar vacío.")

        if not self.__documento:
            registrar_error("Documento de cliente vacío.")
            raise ValidacionError("El documento de identidad no puede estar vacío.")

        if not self.__correo:
            registrar_error("Correo de cliente vacío.")
            raise ValidacionError("El correo electrónico no puede estar vacío.")

        if not self.__telefono:
            registrar_error("Teléfono de cliente vacío.")
            raise ValidacionError("El teléfono no puede estar vacío.")

        # 2. Validar que el documento contenga exclusivamente números
        if not self.__documento.isdigit():
            registrar_error(f"Documento inválido: {self.__documento}")
            raise ValidacionError("El documento debe contener solo números.")

        # 3. Robustecer validación de Correo Electrónico (Debe tener '@' y al menos un '.' posterior)
        if "@" not in self.__correo or "." not in self.__correo.split("@")[-1]:
            registrar_error(f"Correo inválido: {self.__correo}")
            raise ValidacionError("El formato del correo electrónico es inválido (ej: usuario@dominio.com).")

        # 4. Validar que el teléfono sea puramente numérico
        if not self.__telefono.isdigit():
            registrar_error(f"Teléfono inválido: {self.__telefono}")
            raise ValidacionError("El teléfono debe contener solo números.")

        registrar_info(f"Cliente registrado correctamente: {self.__nombre}")

    @property
    def nombre(self):
        return self.__nombre

    @property
    def documento(self):
        return self.__documento

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def mostrar_info(self):
        return (
            f"ID: {self.id}\n"
            f"Nombre: {self.__nombre}\n"
            f"Documento: {self.__documento}\n"
            f"Correo: {self.__correo}\n"
            f"Telefono: {self.__telefono}"
        )
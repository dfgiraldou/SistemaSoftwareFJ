"""
Excepciones personalizadas del sistema Software FJ
"""


class SoftwareFJError(Exception):
    """
    Excepción base para todos los errores propios del dominio
    del sistema Software FJ. Permite capturar cualquier error de
    negocio con un único except si es necesario, sin perder la
    especificidad de cada subclase.
    """
    pass


class ClienteError(SoftwareFJError):
    """Errores relacionados con la validación o gestión de clientes."""
    pass


class ServicioError(SoftwareFJError):
    """Errores relacionados con la creación o cálculo de servicios."""
    pass


class ReservaError(SoftwareFJError):
    """Errores relacionados con la creación o procesamiento de reservas."""
    pass


class ValidacionError(SoftwareFJError):
    """Errores de validación de datos de entrada en general."""
    pass


class OperacionError(SoftwareFJError):
    """Errores por operaciones no permitidas (ej. confirmar/cancelar en estado inválido)."""
    pass
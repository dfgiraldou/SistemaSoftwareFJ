import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/sistema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


def registrar_info(mensaje):
    logging.info(mensaje)


def registrar_error(mensaje, exc_info=False):
    """
    exc_info=True permite adjuntar el traceback completo al log,
    útil cuando se registra una excepción encadenada (raise ... from ...).
    """
    logging.error(mensaje, exc_info=exc_info)
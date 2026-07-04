"""
Pruebas de excepciones del Sistema Software FJ
"""

from modelos.cliente import Cliente
from excepciones.excepciones import ValidacionError


try:

    cliente = Cliente(
        1,
        "",
        "12345678",
        "correo@correo.com",
        "3001234567"
    )

except ValidacionError as error:

    print(f"Error detectado: {error}")

else:

    print("Cliente creado correctamente")

finally:

    print("Fin de la prueba")
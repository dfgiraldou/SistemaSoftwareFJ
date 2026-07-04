# Sistema Integral Software FJ

Sistema de gestión de clientes, servicios y reservas para la empresa ficticia **Software FJ**, desarrollado en Python aplicando los principios de la Programación Orientada a Objetos (POO): abstracción, herencia, polimorfismo y encapsulación, junto con manejo avanzado de excepciones.

Este proyecto fue desarrollado como parte de la Actividad 4 (Fase 4) del curso **Programación (213023)** de la Universidad Nacional Abierta y a Distancia (UNAD).

## Integrantes del equipo

- Veronica Valencia Cortez
- Jefferson Matabanchoy Lectamo
- David Ferney Giraldo Uribe

**Docente:** Carlos Andrés Pinilla Díaz

## Descripción del proyecto

El sistema permite gestionar de forma completa:

- **Clientes**: registro con validaciones estrictas (documento, correo, teléfono).
- **Servicios**: tres tipos especializados que heredan de una clase abstracta común:
  - Asesoría especializada
  - Alquiler de equipo
  - Reserva de sala
- **Reservas**: vinculan un cliente con un servicio, permitiendo confirmar, cancelar y procesar el cálculo del costo.

Toda la información se gestiona **en memoria**, mediante objetos y listas, sin uso de bases de datos. El manejo de errores se realiza mediante excepciones personalizadas y se registra en un archivo de logs (`logs/sistema.log`).

## Tecnologías utilizadas

- **Python 3**
- **Tkinter** (interfaz gráfica)
- **Módulo `logging`** (registro de eventos y errores)
- **Programación Orientada a Objetos** (clases abstractas, herencia, polimorfismo, encapsulación)

## Estructura del proyecto
SistemaSoftwareFJ/
│
├── modelos/
│   ├── entidad.py          # Clase abstracta base del sistema
│   ├── cliente.py          # Clase Cliente con validaciones
│   ├── servicio.py         # Clase abstracta Servicio
│   ├── asesoria.py         # Servicio especializado: Asesoría
│   ├── alquiler_equipo.py  # Servicio especializado: Alquiler de Equipo
│   ├── reserva_sala.py     # Servicio especializado: Reserva de Sala
│   ├── reserva.py          # Clase Reserva
│   └── sistema_fj.py       # Administrador general del sistema
│
├── excepciones/
│   └── excepciones.py      # Excepciones personalizadas del sistema
│
├── logs/
│   ├── config_log.py       # Configuración del sistema de logs
│   └── sistema.log         # Archivo generado con el registro de eventos
│
├── interfaz/
│   └── ventana_principal.py  # Interfaz gráfica (Tkinter)
│
├── pruebas_excepciones/    # Pruebas del manejo de excepciones
│
├── main.py                 # Punto de entrada de la aplicación
├── .gitignore
└── README.md
## Cómo ejecutar el proyecto

1. Clonar el repositorio:
```bash
   git clone https://github.com/dfgiraldou/SistemaSoftwareFJ.git
```
2. Ingresar a la carpeta del proyecto:
```bash
   cd SistemaSoftwareFJ
```
3. Ejecutar la aplicación:
```bash
   python main.py
```

No se requieren librerías externas adicionales; el proyecto utiliza únicamente módulos estándar de Python (`tkinter`, `logging`, `abc`, `datetime`).

## Funcionalidades principales

- **Registrar Cliente**: crea un nuevo cliente con validaciones (nombre, documento, correo, teléfono).
- **Crear Servicio**: permite crear cualquiera de los tres tipos de servicio disponibles.
- **Crear Reserva**: vincula un cliente existente con un servicio existente.
- **Ver Registros**: muestra en una ventana con pestañas todos los clientes, servicios y reservas guardados durante la ejecución.
- **Ejecutar Simulaciones (10 Op.)**: simula automáticamente 10 operaciones (registros válidos e inválidos) para demostrar el manejo de excepciones y la estabilidad del sistema.

## Manejo de excepciones

El sistema implementa una jerarquía de excepciones personalizadas (`SoftwareFJError` y sus subclases: `ClienteError`, `ServicioError`, `ReservaError`, `ValidacionError`, `OperacionError`), junto con bloques `try/except/else/finally` y encadenamiento de excepciones (`raise ... from ...`), garantizando que el sistema permanezca estable ante errores como datos inválidos, parámetros faltantes o cálculos inconsistentes.

Todos los eventos y errores relevantes quedan registrados en `logs/sistema.log`.

## Licencia

Proyecto desarrollado con fines académicos para la UNAD.

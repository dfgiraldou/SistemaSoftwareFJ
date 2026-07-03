import tkinter as tk
from tkinter import messagebox
import inspect

from modelos.cliente import Cliente
from modelos.sistema_fj import SistemaFJ
from excepciones.excepciones import ValidacionError

# IMPORTAMOS LOS MODELOS DE SERVICIO PARA INYECTARLES EL MÉTODO DE COMPARACIÓN A NIVEL DE CLASE
from modelos.alquiler_equipo import AlquilerEquipo
from modelos.asesoria import Asesoria

def _mapear_menor_igual_clase(self, otro):
    """
    Método universal adjuntado a la clase para que cuando el modelo intente hacer
    'servicio <= entero', use el precio interno numérico en su lugar.
    """
    val_propio = getattr(self, 'precio', 0)
    if val_propio == 0:
        val_propio = getattr(self, '_precio', 0)
        
    if isinstance(otro, (int, float)):
        return val_propio <= otro
        
    val_otro = getattr(otro, 'precio', 0) if hasattr(otro, 'precio') else getattr(otro, '_precio', 0)
    return val_propio <= val_otro

# Inyección directa en la estructura de la clase para corregir el comportamiento en Python
AlquilerEquipo.__le__ = _mapear_menor_igual_clase
Asesoria.__le__ = _mapear_menor_igual_clase


class VentanaPrincipal:
    """
    Interfaz gráfica principal del sistema Integral Software FJ.
    """

    def __init__(self):
        self.ventana = tk.Tk()
        self.sistema = SistemaFJ()
        
        self.ventana.title("Sistema Integral Software FJ")
        self.ventana.geometry("700x580")
        self.ventana.resizable(False, False)
        
        titulo = tk.Label(
            self.ventana,
            text="Sistema Integral Software FJ",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=20)
        
# Botón que abre la ventana para registrar un nuevo cliente.
# # Al hacer clic, ejecuta el método registrar_cliente().

        boton_cliente = tk.Button(
            self.ventana,
            text="Registrar Cliente",
            width=30,
            command=self.registrar_cliente
        )        
        boton_cliente.pack(pady=8)

# Botón que abre la ventana para crear un nuevo servici
# (Asesoría o Alquiler de Equipo).
# Al hacer clic, ejecuta el método crear_servicio().        
        boton_servicio = tk.Button(
            self.ventana,
            text="Crear Servicio",
            width=30,
            command=self.crear_servicio
        )        
        boton_servicio.pack(pady=8)
        
# Botón que abre la ventana para crear una nueva reserva,
# asociando un cliente con un servicio registrado.
# Al hacer clic, ejecuta el método crear_reserva().        
        boton_reserva = tk.Button(
            self.ventana,
            text="Crear Reserva",
            width=30,
            command=self.crear_reserva
        )
        boton_reserva.pack(pady=8)

# Botón que ejecuta las 10 operaciones de prueba requeridas
# para verificar el correcto funcionamiento del sistema.
# Al hacer clic, ejecuta el método ejecutar_simulacion_automatica().
        boton_simulacion = tk.Button(
            self.ventana,
            text="Ejecutar Simulaciones (10 Op.)",
            width=30,
            bg="#d4edda",
            fg="#155724",
            font=("Arial", 10, "bold"),
            command=self.ejecutar_simulacion_automatica
        )
        boton_simulacion.pack(pady=15)
        
# Botón que cierra la aplicación y finaliza la ejecución del sistema.
# Al hacer clic, destruye la ventana principal.        
        boton_salir = tk.Button(
            self.ventana,
            text="Salir",
            width=30,
            command=self.ventana.destroy
        )
        boton_salir.pack(pady=15)
        

    def _obtener_lista_clientes(self):
        """Intenta leer la lista de clientes adaptándose a la estructura interna de SistemaFJ."""
        for attr in ['clientes', 'listar_clientes', '_SistemaFJ__clientes']:
            if hasattr(self.sistema, attr):
                valor = getattr(self.sistema, attr)
                return valor() if callable(valor) else valor
        return []

    def _obtener_lista_servicios(self):
        """Intenta leer la lista de servicios adaptándose a la estructura interna de SistemaFJ."""
        for attr in ['servicios', 'listar_servicios', '_SistemaFJ__servicios']:
            if hasattr(self.sistema, attr):
                valor = getattr(self.sistema, attr)
                return valor() if callable(valor) else valor
        return []

    def _obtener_lista_reservas(self):
        """Intenta leer la lista de reservas adaptándose a la estructura interna de SistemaFJ."""
        for attr in ['reservas', 'listar_reservas', '_SistemaFJ__reservas']:
            if hasattr(self.sistema, attr):
                valor = getattr(self.sistema, attr)
                return valor() if callable(valor) else valor
        return []
        
    def _instanciar_con_firma(self, clase_destino, id_reserva, cliente, servicio, duracion, fecha, precio):
        """
        Inspecciona el constructor (__init__) de la clase Reserva para pasarle
        los parámetros exactamente en el orden posicional que sus campos exigen.
        """
        sig = inspect.signature(clase_destino.__init__)
        parametros = list(sig.parameters.keys())[1:] # Omitimos 'self'
        num_esperados = len(parametros)

        # Mapeo inteligente según el nombre que tenga el argumento en el modelo original
        valores_disponibles = {
            'id': id_reserva, 'id_reserva': id_reserva,
            'cliente': cliente,
            'servicio': servicio,
            'duracion': duracion, 'tiempo': duracion,
            'fecha': fecha, 'detalles': fecha,
            'precio': precio, 'costo': precio, 'valor': precio
        }

        args_a_pasar = []
        for i, param in enumerate(parametros):
            if param in valores_disponibles:
                args_a_pasar.append(valores_disponibles[param])
            else:
                # Si no coincide el nombre exacto, asignamos por orden por defecto alternativo
                valores_por_defecto_orden = [id_reserva, cliente, servicio, duracion, fecha, precio]
                if i < len(valores_por_defecto_orden):
                    args_a_pasar.append(valores_por_defecto_orden[i])

        # Recorte de seguridad según los argumentos que acepte el inicializador de la clase
        return clase_destino(*args_a_pasar[:num_esperados])
        
    def registrar_cliente(self):
        ventana_cliente = tk.Toplevel(self.ventana)
        ventana_cliente.title("Registrar Cliente")
        ventana_cliente.geometry("400x350")
        ventana_cliente.resizable(False, False)
        
        def solo_letras(texto):
            return texto == "" or all(c.isalpha() or c.isspace() for c in texto)
        
        validacion_nombre = self.ventana.register(solo_letras)

        tk.Label(ventana_cliente, text="Nombre:").pack(pady=5)
        entrada_nombre = tk.Entry(
            ventana_cliente, 
            width=35,
            validate="key",
            validatecommand=(validacion_nombre, "%P")
        )
        entrada_nombre.pack(pady=5)
        
        tk.Label(ventana_cliente, text="Documento:").pack(pady=5)
        entrada_documento = tk.Entry(ventana_cliente, width=35)
        entrada_documento.pack()
        
        tk.Label(ventana_cliente, text="Correo:").pack(pady=5)
        entrada_correo = tk.Entry(ventana_cliente, width=35)
        entrada_correo.pack()
        
        tk.Label(ventana_cliente, text="Teléfono:").pack(pady=5)
        entrada_telefono = tk.Entry(ventana_cliente, width=35)
        entrada_telefono.pack()
        
        def guardar_cliente():
            try:
                id_cliente = len(self._obtener_lista_clientes()) + 1
                cliente = Cliente(
                    id_cliente,
                    entrada_nombre.get(),
                    entrada_documento.get(),
                    entrada_correo.get(),
                    entrada_telefono.get(),
                )
                self.sistema.agregar_cliente(cliente)
                
            except ValidacionError as error:
                messagebox.showerror("Error de Validación", str(error))
            except Exception as error:  
                messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{error}")  
            else:
                messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
                ventana_cliente.destroy()
            finally:
                print("Intento de registro de cliente procesado.")
                
        boton_guardar = tk.Button(
            ventana_cliente, text="Guardar", width=20, command=guardar_cliente
        )
        boton_guardar.pack(pady=20)

    def crear_servicio(self):
        ventana_servicio = tk.Toplevel(self.ventana)
        ventana_servicio.title("Crear Servicio")
        ventana_servicio.geometry("400x420")
        ventana_servicio.resizable(False, False)

        tk.Label(ventana_servicio, text="Tipo de Servicio:").pack(pady=5)
        var_tipo = tk.StringVar(ventana_servicio)
        var_tipo.set("Asesoría")
        
        label_tipo_equipo = tk.Label(ventana_servicio, text="Especificar Tipo de Equipo (ej: Portátil):")
        entrada_tipo_equipo = tk.Entry(ventana_servicio, width=35)

        def alternar_campos(*args):
            if var_tipo.get() == "Alquiler de Equipo":
                label_tipo_equipo.pack(pady=5)
                entrada_tipo_equipo.pack(pady=5)
            else:
                label_tipo_equipo.pack_forget()
                entrada_tipo_equipo.pack_forget()

        var_tipo.trace_add("write", alternar_campos)

        menu_tipo = tk.OptionMenu(ventana_servicio, var_tipo, "Asesoría", "Alquiler de Equipo")
        menu_tipo.pack(pady=5)

        tk.Label(ventana_servicio, text="Nombre/Descripción del Servicio:").pack(pady=5)
        entrada_nombre = tk.Entry(ventana_servicio, width=35)
        entrada_nombre.pack(pady=5)

        tk.Label(ventana_servicio, text="Precio/Tarifa ($):").pack(pady=5)
        entrada_precio = tk.Entry(ventana_servicio, width=35)
        entrada_precio.pack(pady=5)

        def guardar_servicio():
            try:
                id_servicio = len(self._obtener_lista_servicios()) + 1
                tipo = var_tipo.get()
                nombre = entrada_nombre.get()
                precio_raw = entrada_precio.get()

                try:
                    precio = float(precio_raw) if '.' in precio_raw else int(precio_raw)
                except ValueError:
                    raise ValidacionError("El precio/tarifa debe ser un valor numérico válido.")

                if tipo == "Asesoría":
                    nuevo_servicio = Asesoria(id_servicio, nombre, precio)
                else:
                    tipo_eq = entrada_tipo_equipo.get()
                    if not tipo_eq.strip():
                        raise ValidacionError("Debe especificar el tipo de equipo a alquilar.")
                    nuevo_servicio = AlquilerEquipo(id_servicio, nombre, precio, tipo_eq)

                self.sistema.agregar_servicio(nuevo_servicio)
                
            except ValidacionError as error:
                messagebox.showerror("Error de Validación", str(error))
            except Exception as error:
                messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{error}")
            else:
                messagebox.showinfo("Éxito", f"Servicio de {tipo} creado correctamente.")
                ventana_servicio.destroy()
            finally:
                print("Intento de creación de servicio procesado.")

        boton_guardar = tk.Button(
            ventana_servicio, text="Guardar", width=20, command=guardar_servicio
        )
        boton_guardar.pack(pady=20)
        
        alternar_campos()

    def crear_reserva(self):
        from modelos.reserva import Reserva
        from modelos.reserva_sala import ReservaSala

        lista_clientes = self._obtener_lista_clientes()
        lista_servicios = self._obtener_lista_servicios()

        if not lista_clientes or not lista_servicios:
            messagebox.showwarning(
                "Datos Faltantes", 
                "Debe registrar al menos un cliente y un servicio antes de crear una reserva."
            )
            return

        ventana_reserva = tk.Toplevel(self.ventana)
        ventana_reserva.title("Crear Reserva")
        ventana_reserva.geometry("400x450")
        ventana_reserva.resizable(False, False)

        dict_clientes = {f"{c.nombre} (Doc: {c.documento})": c for c in lista_clientes}
        dict_servicios = {f"{s.nombre}": s for s in lista_servicios}

        tk.Label(ventana_reserva, text="Seleccione el Cliente:").pack(pady=5)
        var_cliente = tk.StringVar(ventana_reserva)
        var_cliente.set(list(dict_clientes.keys())[0])
        menu_cliente = tk.OptionMenu(ventana_reserva, var_cliente, *dict_clientes.keys())
        menu_cliente.pack(pady=5)

        tk.Label(ventana_reserva, text="Seleccione el Servicio:").pack(pady=5)
        var_servicio = tk.StringVar(ventana_reserva)
        var_servicio.set(list(dict_servicios.keys())[0])
        menu_servicio = tk.OptionMenu(ventana_reserva, var_servicio, *dict_servicios.keys())
        menu_servicio.pack(pady=5)

        tk.Label(ventana_reserva, text="Tipo de Reserva:").pack(pady=5)
        var_tipo_reserva = tk.StringVar(ventana_reserva)
        var_tipo_reserva.set("General")
        menu_tipo_reserva = tk.OptionMenu(ventana_reserva, var_tipo_reserva, "General", "Reserva de Sala")
        menu_tipo_reserva.pack(pady=5)

        tk.Label(ventana_reserva, text="Duración (en días o horas según su regla):").pack(pady=5)
        entrada_duracion = tk.Entry(ventana_reserva, width=35)
        entrada_duracion.pack(pady=5)

        tk.Label(ventana_reserva, text="Fecha / Detalles Extra:").pack(pady=5)
        entrada_fecha = tk.Entry(ventana_reserva, width=35)
        entrada_fecha.pack(pady=5)

        def guardar_reserva():
            try:
                id_reserva = len(self._obtener_lista_reservas()) + 1
                cliente_sel = dict_clientes.get(var_cliente.get())
                servicio_sel = dict_servicios.get(var_servicio.get())
                fecha = entrada_fecha.get()
                tipo_r = var_tipo_reserva.get()

                try:
                    duracion = int(entrada_duracion.get())
                except ValueError:
                    raise ValidacionError("La duración debe ser un número entero.")

                clase_reserva = Reserva if tipo_r == "General" else ReservaSala
                
                precio_servicio = getattr(servicio_sel, 'precio', 0)
                if precio_servicio == 0:
                    precio_servicio = getattr(servicio_sel, '_precio', 0)

                # Instanciación segura mapeando de forma inteligente cada campo por nombre
                nueva_reserva = self._instanciar_con_firma(
                    clase_reserva, id_reserva, cliente_sel, servicio_sel, duracion, fecha, precio_servicio
                )

                self.sistema.agregar_reserva(nueva_reserva)
                
            except ValidacionError as error:
                messagebox.showerror("Error de Validación", str(error))
            except Exception as error:
                messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{error}")
            else:
                messagebox.showinfo("Éxito", "Reserva registrada correctamente.")
                ventana_reserva.destroy()
            finally:
                print("Intento de registro de reserva procesado.")

        boton_guardar = tk.Button(
            ventana_reserva, text="Guardar", width=20, command=guardar_reserva
        )
        boton_guardar.pack(pady=15)

    def ejecutar_simulacion_automatica(self):
        """
        Simula en lote las 10 operaciones requeridas por la guía, manejando
        correctamente las firmas dinámicas y conversiones numéricas.
        """
        from modelos.reserva import Reserva

        operaciones_exitosas = 0
        operaciones_fallidas = 0

        pruebas = [
            ("CLIENTE_OK", ("Veronica Valencia", "12345678", "veronica@unad.edu.co", "310123456")),
            ("CLIENTE_ERR_NOM", ("", "87654321", "error@correo.com", "300111222")),
            ("CLIENTE_ERR_DOC", ("Pedro Perez", "ABC1234", "pedro@correo.com", "300333444")),
            ("CLIENTE_OK", ("Loren Gomez", "98765432", "loren@gmail.com", "315999888")),
            
            ("SERVICIO_OK", ("ASESORIA", "Asesoría en Sistemas Integrales", 150000)),
            ("SERVICIO_ERR_PRE", ("ALQUILER", "Alquiler Computador Portátil", "Gratis")),
            ("SERVICIO_OK", ("ALQUILER", "Alquiler Sala de Conferencias A", 85000)),
            
            ("RESERVA_OK", (0, 0, 1, "15/07/2026")),
            ("RESERVA_ERR_CLI", (None, 0, 1, "20/07/2026")),
            ("RESERVA_ERR_FEC", (0, 0, 1, ""))
        ]

        for tipo, datos in pruebas:
            try:
                if "CLIENTE" in tipo:
                    id_c = len(self._obtener_lista_clientes()) + 1
                    obj = Cliente(id_c, datos[0], datos[1], datos[2], datos[3])
                    self.sistema.agregar_cliente(obj)
                    
                elif "SERVICIO" in tipo:
                    id_s = len(self._obtener_lista_servicios()) + 1
                    try:
                        precio = int(datos[2]) if isinstance(datos[2], (int, float)) else int(datos[2])
                    except ValueError:
                        raise ValidacionError("Precio inválido en simulación.")

                    if datos[0] == "ASESORIA":
                        obj = Asesoria(id_s, datos[1], precio)
                    else:
                        obj = AlquilerEquipo(id_s, datos[1], precio, "Computador")
                    self.sistema.agregar_servicio(obj)
                    
                elif "RESERVA" in tipo:
                    id_r = len(self._obtener_lista_reservas()) + 1
                    cli = self._obtener_lista_clientes()[datos[0]] if datos[0] is not None else None
                    srv = self._obtener_lista_servicios()[datos[1]] if datos[1] is not None else None
                    
                    p_srv = getattr(srv, 'precio', 0) if srv else 0
                    obj = self._instanciar_con_firma(Reserva, id_r, cli, srv, datos[2], datos[3], p_srv)
                    self.sistema.agregar_reserva(obj)
                
                operaciones_exitosas += 1
            except Exception:
                operaciones_fallidas += 1

        messagebox.showinfo(
            "Simulación Completada",
            f"Se han ejecutado las 10 operaciones de simulación:\n\n"
            f"✔️ Operaciones Exitosas: {operaciones_exitosas}\n"
            f"❌ Excepciones Controladas: {operaciones_fallidas}\n\n"
            f"Revise el archivo de logs para comprobar el correcto registro de eventos."
        )

    def ejecutar(self):
        """
        Ejecuta la ventana principal.
        """
        self.ventana.mainloop()



import tkinter as tk
from tkinter import messagebox, ttk

from modelos.cliente import Cliente
from modelos.asesoria import Asesoria
from modelos.alquiler_equipo import AlquilerEquipo
from modelos.reserva_sala import ReservaSala
from modelos.reserva import Reserva
from modelos.sistema_fj import SistemaFJ
from excepciones.excepciones import SoftwareFJError


class VentanaPrincipal:
    """
    Interfaz gráfica principal del sistema Integral Software FJ.
    """

    def __init__(self):
        self.ventana = tk.Tk()
        self.sistema = SistemaFJ()

        self.ventana.title("Sistema Integral Software FJ")
        self.ventana.geometry("700x620")
        self.ventana.resizable(False, False)

        titulo = tk.Label(
            self.ventana,
            text="Sistema Integral Software FJ",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=20)

        tk.Button(
            self.ventana, text="Registrar Cliente", width=30,
            command=self.registrar_cliente
        ).pack(pady=8)

        tk.Button(
            self.ventana, text="Crear Servicio", width=30,
            command=self.crear_servicio
        ).pack(pady=8)

        tk.Button(
            self.ventana, text="Crear Reserva", width=30,
            command=self.crear_reserva
        ).pack(pady=8)

        tk.Button(
            self.ventana, text="Ver Registros", width=30,
            command=self.ver_registros
        ).pack(pady=8)

        tk.Button(
            self.ventana, text="Ejecutar Simulaciones (10 Op.)", width=30,
            bg="#d4edda", fg="#155724", font=("Arial", 10, "bold"),
            command=self.ejecutar_simulacion_automatica
        ).pack(pady=15)

        tk.Button(
            self.ventana, text="Salir", width=30,
            command=self.ventana.destroy
        ).pack(pady=15)

    # ------------------------------------------------------------------
    # Registrar Cliente
    # ------------------------------------------------------------------
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
            ventana_cliente, width=35,
            validate="key", validatecommand=(validacion_nombre, "%P")
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
                id_cliente = self.sistema.generar_id_cliente()
                cliente = Cliente(
                    id_cliente,
                    entrada_nombre.get(),
                    entrada_documento.get(),
                    entrada_correo.get(),
                    entrada_telefono.get(),
                )
                self.sistema.agregar_cliente(cliente)

            except SoftwareFJError as error:
                messagebox.showerror("Error de Validación", str(error))
            except Exception as error:
                messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{error}")
            else:
                messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
                ventana_cliente.destroy()
            finally:
                print("Intento de registro de cliente procesado.")

        tk.Button(
            ventana_cliente, text="Guardar", width=20, command=guardar_cliente
        ).pack(pady=20)

    # ------------------------------------------------------------------
    # Crear Servicio
    # ------------------------------------------------------------------
    def crear_servicio(self):
        ventana_servicio = tk.Toplevel(self.ventana)
        ventana_servicio.title("Crear Servicio")
        ventana_servicio.geometry("400x460")
        ventana_servicio.resizable(False, False)

        tk.Label(ventana_servicio, text="Tipo de Servicio:").pack(pady=5)
        var_tipo = tk.StringVar(ventana_servicio)
        var_tipo.set("Asesoría")

        label_extra = tk.Label(ventana_servicio, text="")
        entrada_extra = tk.Entry(ventana_servicio, width=35)

        def alternar_campos(*args):
            tipo = var_tipo.get()
            if tipo == "Alquiler de Equipo":
                label_extra.config(text="Tipo de Equipo (ej: Portátil):")
                label_extra.pack(pady=5)
                entrada_extra.pack(pady=5)
            elif tipo == "Reserva de Sala":
                label_extra.config(text="Capacidad (número de personas):")
                label_extra.pack(pady=5)
                entrada_extra.pack(pady=5)
            else:  # Asesoría
                label_extra.config(text="Especialidad (ej: Sistemas):")
                label_extra.pack(pady=5)
                entrada_extra.pack(pady=5)

        var_tipo.trace_add("write", alternar_campos)

        menu_tipo = tk.OptionMenu(
            ventana_servicio, var_tipo,
            "Asesoría", "Alquiler de Equipo", "Reserva de Sala"
        )
        menu_tipo.pack(pady=5)

        tk.Label(ventana_servicio, text="Nombre/Descripción del Servicio:").pack(pady=5)
        entrada_nombre = tk.Entry(ventana_servicio, width=35)
        entrada_nombre.pack(pady=5)

        tk.Label(ventana_servicio, text="Costo Base ($):").pack(pady=5)
        entrada_costo = tk.Entry(ventana_servicio, width=35)
        entrada_costo.pack(pady=5)

        def guardar_servicio():
            try:
                id_servicio = self.sistema.generar_id_servicio()
                tipo = var_tipo.get()
                nombre = entrada_nombre.get()
                costo_raw = entrada_costo.get()

                try:
                    costo_base = float(costo_raw)
                except ValueError:
                    raise SoftwareFJError("El costo base debe ser un valor numérico válido.")

                if tipo == "Asesoría":
                    nuevo_servicio = Asesoria(id_servicio, nombre, costo_base, entrada_extra.get())

                elif tipo == "Alquiler de Equipo":
                    nuevo_servicio = AlquilerEquipo(id_servicio, nombre, costo_base, entrada_extra.get())

                else:  # Reserva de Sala
                    try:
                        capacidad = int(entrada_extra.get())
                    except ValueError:
                        raise SoftwareFJError("La capacidad debe ser un número entero.")
                    nuevo_servicio = ReservaSala(id_servicio, nombre, costo_base, capacidad)

                self.sistema.agregar_servicio(nuevo_servicio)

            except SoftwareFJError as error:
                messagebox.showerror("Error de Validación", str(error))
            except Exception as error:
                messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{error}")
            else:
                messagebox.showinfo("Éxito", f"Servicio de {tipo} creado correctamente.")
                ventana_servicio.destroy()
            finally:
                print("Intento de creación de servicio procesado.")

        tk.Button(
            ventana_servicio, text="Guardar", width=20, command=guardar_servicio
        ).pack(pady=20)

        alternar_campos()

    # ------------------------------------------------------------------
    # Crear Reserva
    # ------------------------------------------------------------------
    def crear_reserva(self):
        lista_clientes = self.sistema.listar_clientes()
        lista_servicios = self.sistema.listar_servicios()

        if not lista_clientes or not lista_servicios:
            messagebox.showwarning(
                "Datos Faltantes",
                "Debe registrar al menos un cliente y un servicio antes de crear una reserva."
            )
            return

        ventana_reserva = tk.Toplevel(self.ventana)
        ventana_reserva.title("Crear Reserva")
        ventana_reserva.geometry("400x350")
        ventana_reserva.resizable(False, False)

        dict_clientes = {f"{c.nombre} (Doc: {c.documento})": c for c in lista_clientes}
        dict_servicios = {f"{s.nombre} - {s.describir()}": s for s in lista_servicios}

        tk.Label(ventana_reserva, text="Seleccione el Cliente:").pack(pady=5)
        var_cliente = tk.StringVar(ventana_reserva)
        var_cliente.set(list(dict_clientes.keys())[0])
        tk.OptionMenu(ventana_reserva, var_cliente, *dict_clientes.keys()).pack(pady=5)

        tk.Label(ventana_reserva, text="Seleccione el Servicio:").pack(pady=5)
        var_servicio = tk.StringVar(ventana_reserva)
        var_servicio.set(list(dict_servicios.keys())[0])
        tk.OptionMenu(ventana_reserva, var_servicio, *dict_servicios.keys()).pack(pady=5)

        tk.Label(ventana_reserva, text="Duración (horas/días según el servicio):").pack(pady=5)
        entrada_duracion = tk.Entry(ventana_reserva, width=35)
        entrada_duracion.pack(pady=5)

        def guardar_reserva():
            try:
                id_reserva = self.sistema.generar_id_reserva()
                cliente_sel = dict_clientes.get(var_cliente.get())
                servicio_sel = dict_servicios.get(var_servicio.get())

                try:
                    duracion = int(entrada_duracion.get())
                except ValueError:
                    raise SoftwareFJError("La duración debe ser un número entero.")

                nueva_reserva = Reserva(id_reserva, cliente_sel, servicio_sel, duracion)
                self.sistema.agregar_reserva(nueva_reserva)

            except SoftwareFJError as error:
                messagebox.showerror("Error de Validación", str(error))
            except Exception as error:
                messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{error}")
            else:
                messagebox.showinfo("Éxito", "Reserva registrada correctamente.")
                ventana_reserva.destroy()
            finally:
                print("Intento de registro de reserva procesado.")

        tk.Button(
            ventana_reserva, text="Guardar", width=20, command=guardar_reserva
        ).pack(pady=15)

    # ------------------------------------------------------------------
    # Ver Registros
    # ------------------------------------------------------------------
    def ver_registros(self):
        ventana_registros = tk.Toplevel(self.ventana)
        ventana_registros.title("Registros del Sistema")
        ventana_registros.geometry("650x450")
        ventana_registros.resizable(False, False)

        notebook = ttk.Notebook(ventana_registros)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # --- Pestaña Clientes ---
        frame_clientes = ttk.Frame(notebook)
        notebook.add(frame_clientes, text="Clientes")

        columnas_cliente = ("id", "nombre", "documento", "correo", "telefono")
        tabla_clientes = ttk.Treeview(frame_clientes, columns=columnas_cliente, show="headings")
        for col, titulo in zip(columnas_cliente, ("ID", "Nombre", "Documento", "Correo", "Teléfono")):
            tabla_clientes.heading(col, text=titulo)
            tabla_clientes.column(col, width=110)
        tabla_clientes.pack(expand=True, fill="both")

        for c in self.sistema.listar_clientes():
            tabla_clientes.insert("", "end", values=(c.id, c.nombre, c.documento, c.correo, c.telefono))

        # --- Pestaña Servicios ---
        frame_servicios = ttk.Frame(notebook)
        notebook.add(frame_servicios, text="Servicios")

        columnas_servicio = ("id", "tipo", "nombre", "costo_base", "detalle")
        tabla_servicios = ttk.Treeview(frame_servicios, columns=columnas_servicio, show="headings")
        for col, titulo in zip(columnas_servicio, ("ID", "Tipo", "Nombre", "Costo Base", "Detalle")):
            tabla_servicios.heading(col, text=titulo)
            tabla_servicios.column(col, width=110)
        tabla_servicios.pack(expand=True, fill="both")

        for s in self.sistema.listar_servicios():
            tabla_servicios.insert(
                "", "end",
                values=(s.id, type(s).__name__, s.nombre, f"${s.costo_base:,.2f}", s.describir())
            )

        # --- Pestaña Reservas ---
        frame_reservas = ttk.Frame(notebook)
        notebook.add(frame_reservas, text="Reservas")

        columnas_reserva = ("id", "cliente", "servicio", "duracion", "estado")
        tabla_reservas = ttk.Treeview(frame_reservas, columns=columnas_reserva, show="headings")
        for col, titulo in zip(columnas_reserva, ("ID", "Cliente", "Servicio", "Duración", "Estado")):
            tabla_reservas.heading(col, text=titulo)
            tabla_reservas.column(col, width=110)
        tabla_reservas.pack(expand=True, fill="both")

        for r in self.sistema.listar_reservas():
            tabla_reservas.insert(
                "", "end",
                values=(r.id, r.cliente.nombre, r.servicio.nombre, r.duracion, r.estado)
            )

        tk.Button(
            ventana_registros, text="Cerrar", width=20,
            command=ventana_registros.destroy
        ).pack(pady=10)

    # ------------------------------------------------------------------
    # Simulación automática (10 operaciones)
    # ------------------------------------------------------------------
    def ejecutar_simulacion_automatica(self):
        """
        Simula en lote las 10 operaciones requeridas por la guía:
        registros válidos e inválidos de clientes, servicios y reservas.
        """
        operaciones_exitosas = 0
        operaciones_fallidas = 0

        pruebas = [
            ("CLIENTE_OK", ("Veronica Valencia", "12345678", "veronica@unad.edu.co", "310123456")),
            ("CLIENTE_ERR_NOM", ("", "87654321", "error@correo.com", "300111222")),
            ("CLIENTE_ERR_DOC", ("Pedro Perez", "ABC1234", "pedro@correo.com", "300333444")),
            ("CLIENTE_OK", ("Loren Gomez", "98765432", "loren@gmail.com", "315999888")),

            ("SERVICIO_ASESORIA_OK", ("Asesoría en Sistemas Integrales", 150000, "Sistemas")),
            ("SERVICIO_ALQUILER_ERR_COSTO", ("Alquiler Computador Portátil", "Gratis", "Portátil")),
            ("SERVICIO_SALA_OK", ("Sala de Conferencias A", 85000, 20)),

            ("RESERVA_OK", (0, 0, 2)),
            ("RESERVA_ERR_CLI", (None, 0, 2)),
            ("RESERVA_ERR_DURACION", (0, 0, -1)),
        ]

        for tipo, datos in pruebas:
            try:
                if tipo.startswith("CLIENTE"):
                    id_c = self.sistema.generar_id_cliente()
                    obj = Cliente(id_c, datos[0], datos[1], datos[2], datos[3])
                    self.sistema.agregar_cliente(obj)

                elif tipo == "SERVICIO_ASESORIA_OK":
                    id_s = self.sistema.generar_id_servicio()
                    obj = Asesoria(id_s, datos[0], datos[1], datos[2])
                    self.sistema.agregar_servicio(obj)

                elif tipo == "SERVICIO_ALQUILER_ERR_COSTO":
                    id_s = self.sistema.generar_id_servicio()
                    try:
                        costo = float(datos[1])
                    except ValueError:
                        raise SoftwareFJError("Costo inválido en simulación.")
                    obj = AlquilerEquipo(id_s, datos[0], costo, datos[2])
                    self.sistema.agregar_servicio(obj)

                elif tipo == "SERVICIO_SALA_OK":
                    id_s = self.sistema.generar_id_servicio()
                    obj = ReservaSala(id_s, datos[0], datos[1], datos[2])
                    self.sistema.agregar_servicio(obj)

                elif tipo.startswith("RESERVA"):
                    id_r = self.sistema.generar_id_reserva()
                    clientes = self.sistema.listar_clientes()
                    servicios = self.sistema.listar_servicios()

                    cli = clientes[datos[0]] if datos[0] is not None and datos[0] < len(clientes) else None
                    srv = servicios[datos[1]] if datos[1] is not None and datos[1] < len(servicios) else None
                    duracion = datos[2]

                    obj = Reserva(id_r, cli, srv, duracion)
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
# Creamos la ventana principal
import tkinter as tk
from tkinter import ttk, messagebox
from models import TicketManager

class HelpdeskUI:
    # Construcción y gestión  de los componentes de la interfaz de usuario
    #1. Le damos un título a nuestra ventana
    #2.Configuramos el tamaño de la ventana (ancho x alto)
    
    def __init__(self, root: tk.Tk, manager: TicketManager):
        self.root = root
        self.manager = manager

        self.root.title("My tickets system help desk ")
        self.root.geometry("950x650")
        self.root.minsize(900, 600)

        # Aplicar estilos
        self.style = ttk.Style()
        self.style.theme_use("classic")

        self._crear_interfaz()
        self.actualizar_tabla()

    def _crear_interfaz(self):
        # Cabecera
        header = ttk.Frame(self.root, padding=12)
        header.pack(fill=tk.X)
        ttk.Label(
            header,
            text="Technical Support Dashbord",
            font=( "Aldhabi", 16, "bold")
        ).pack(side=tk.LEFT)

        # Contenedor Principal
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Formulario a la izquierda
        self._crear_formulario(main_frame)

        # Tabla de controles derecha  
        self._crear_panel_derecho(main_frame)

    def _crear_formulario(self, parent):
        frame = ttk.LabelFrame(parent, text="New ticket", padding=15)
        frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))  

        # Campos 
        ttk.Label(frame, text="User").pack(anchor=tk.W, pady=(2, 6))
        self.ent_usuario = ttk.Entry(frame, width=20)
        self.ent_usuario.pack(fill=tk.X, pady=(2, 10))

        ttk.Label(frame, text="Description").pack(anchor=tk.W, pady=(2, 6))
        self.ent_descripcion = ttk.Entry(frame, width=20)
        self.ent_descripcion.pack(fill=tk.X, pady=(2, 10))

        ttk.Label(frame, text="Category").pack(anchor=tk.W, pady=(2, 6))
        self.cmb_categoria = ttk.Combobox(
            frame,
            values=["Hardware", "Software", "Networks", "Access"],
            state="readonly"
        )
        self.cmb_categoria.set("Hardware")
        self.cmb_categoria.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frame, text="Priority").pack(anchor=tk.W, pady=(0, 5))
        self.cmb_prioridad = ttk.Combobox(
            frame,
            values=["Low", "Medium", "Hight", "Critical"],
            state="readonly"
        )
        self.cmb_prioridad.set("Low")
        self.cmb_prioridad.pack(fill=tk.X, pady=(0, 10))

        # Creo y posiciono los botones
        ttk.Button(frame, text="Create Ticket", command=self._on_crear).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(frame, text="Delete Fields", command=self._limpiar_formulario).pack(fill=tk.X)

    def _crear_panel_derecho(self, parent):
        right_frame = ttk.Frame(parent)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Buscador
        search_frame = ttk.Frame(right_frame) 
        search_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(search_frame, text="Filtrar: ").pack(side=tk.LEFT, padx=(0, 5))
        self.ent_buscar = ttk.Entry(search_frame) 
        self.ent_buscar.pack(side=tk.LEFT, fill=tk.X, expand=True) 
        self.ent_buscar.bind("<KeyRelease>", lambda e: self.actualizar_tabla())

        # Tabla Treeview
        tree_frame = ttk.Frame(right_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "user", "description", "category", "priority", "status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("user", text="User")
        self.tree.heading("description", text="Description")
        self.tree.heading("category", text="Category")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=40, anchor=tk.CENTER)
        self.tree.column("user", width=120)
        self.tree.column("description", width=200)
        self.tree.column("category", width=120)
        self.tree.column("priority", width=80, anchor=tk.CENTER)
        self.tree.column("status", width=80, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Botones de acción 
        actions = ttk.Frame(right_frame, padding=(0, 10, 0, 0))
        actions.pack(fill=tk.X)

        ttk.Button(actions, text="Cambiar estado", command=self._on_cambiar_estado).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(actions, text="Eliminar Ticket", command=self._on_eliminar).pack(side=tk.LEFT)

        # Métricas
        self.lbl_stats = ttk.Label(right_frame, text="", font=("Segoe UI", 9, "italic"))
        self.lbl_stats.pack(anchor=tk.E, pady=(10, 0))

    def _on_crear(self):
        usuario = self.ent_usuario.get().strip()
        descripcion = self.ent_descripcion.get().strip()

        if not usuario or not descripcion:
            messagebox.showwarning("Campos Requeridos", "Por favor completa el Usuario y la Descripción")
            return

        ticket = self.manager.crear_ticket(
            usuario=usuario,
            descripcion=descripcion,
            categoria=self.cmb_categoria.get(),
            prioridad=self.cmb_prioridad.get()
        )

        messagebox.showinfo("Éxito", f"Ticket #{ticket.id} creado correctamente.")
        self._limpiar_formulario()
        self.actualizar_tabla()

    def _on_cambiar_estado(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un ticket primero.")
            return

        ticket_id = int(self.tree.item(selected[0], "values")[0])
        self.manager.cambiar_estado(ticket_id)
        self.actualizar_tabla() 

    def _on_eliminar(self):
        selected = self.tree.selection()  
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un ticket para eliminar.")
            return
        ticket_id = int(self.tree.item(selected[0], "values")[0])
        if messagebox.askyesno("Confirmar", f"¿Deseas borrar el ticket #{ticket_id}?"):
            self.manager.eliminar_ticket(ticket_id)
            self.actualizar_tabla()

    def actualizar_tabla(self):
        # Limpiar
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Datos filtrados
        criterio = self.ent_buscar.get().strip()
        tickets = self.manager.buscar_tickets(criterio)   

        # Insertar filas
        for t in tickets:
            self.tree.insert("", tk.END, values=(
                t.id, t.usuario, t.descripcion, t.categoria, t.prioridad, t.estado
            ))           
        # Actualizar las métricas
        stats = self.manager.obtener_metricas()
        self.lbl_stats.config(
            text=f"Total: {stats['total']} | Pendientes: {stats['pendientes']} | Resueltos: {stats['resueltos']}"
        )

    def _limpiar_formulario(self):
        self.ent_usuario.delete(0, tk.END)
        self.ent_descripcion.delete(0, tk.END)
        self.cmb_categoria.set("Hardware")
        self.cmb_prioridad.set("Media")
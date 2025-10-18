import tkinter as tk
from tkinter import ttk, messagebox
# Importar desde módulos locales
from ..models.order import Order
from ..data.storage import save_orders
from ..utils.basic_time import format_elapsed
from ..utils.time_utils import flash_modified_cards
from ..config import MAX_PREPARING_ORDERS, MAIN_WINDOW_SIZE, ORDER_STATUSES, ORDER_CARD_COLUMNS
from ..ui.order_form import OrderForm
from ..ui.order_card import OrderCard
from ..ui.edit_window import EditWindow
from ..ui.projection import ProjectionWindow
from datetime import datetime #datetime para updated_at en edicion de órdenes

class MainWindow:
    def __init__(self, root, orders):
        self.root = root
        self.orders = orders
        self.tabs = {}
        self.elapsed_vars = {}
        self.flashing_cards = {} 

        self.root.title("Kitchen Orders")
        self.root.geometry(MAIN_WINDOW_SIZE)
        self.root.state("zoomed")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        self.projection_manager = ProjectionWindow(root, self.orders, self.elapsed_vars)

        self._create_tabs()
        self.render_orders()
        self._start_tick()
        
    def _create_tabs(self):
        # Pestaña "Nueva Orden"
        new_order_frame = tk.Frame(self.notebook)
        self.notebook.add(new_order_frame, text="+ Nueva Orden")
        self.tabs["NewOrder"] = new_order_frame
        
        OrderForm(new_order_frame, 
                  self.orders, 
                  self.render_orders, 
                  self.projection_manager.open,
                  self.notebook,
                  save_orders)

        # Pestañas de estado
        for status in ORDER_STATUSES:
            tab_frame = tk.Frame(self.notebook)
            self.notebook.add(tab_frame, text=status)
            
            canvas = tk.Canvas(tab_frame)
            canvas.pack(side="left", fill="both", expand=True)
            
            scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
            scrollbar.pack(side="right", fill="y")
            
            canvas.configure(yscrollcommand=scrollbar.set)
            
            order_container = tk.Frame(canvas)
            canvas.create_window((0, 0), window=order_container, anchor="nw", tags="frame_tag")
            
            def _on_frame_configure(event, canvas=canvas):
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.itemconfig("frame_tag", width=canvas.winfo_width())
            
            order_container.bind("<Configure>", _on_frame_configure)
            
            self.tabs[status] = order_container

    # --- Lógica de Control de Estado y Renderizado ---

    def _save_edit_callback(self, edit_window, order, new_table, new_items_list, new_notes):
        """Implementación del callback para guardar la edición."""
        order.table = new_table
        order.items = new_items_list
        order.notes = new_notes
        
        order.updated_at = datetime.now()
        
        edit_window.destroy()
        save_orders(self.orders)
        self.render_orders()
        self.projection_manager.render()
        
        messagebox.showinfo("Éxito", f"Orden {order.number} actualizada correctamente")
        
    def open_edit_window(self, order):
        """Crea la ventana de edición."""
        EditWindow(self.root, order, self._save_edit_callback)

    def advance_order(self, order):
        """Función para cambiar estado de la orden."""
        if order.status == "Nuevo":
            preparing_count = sum(1 for o in self.orders if o.status == "Preparando")
            if preparing_count >= MAX_PREPARING_ORDERS:
                messagebox.showwarning(
                    "Límite de órdenes en preparación alcanzado",
                    f"Ya hay {preparing_count} órdenes en preparación. \n"
                    "No se pueden agregar más hasta completar algunas"
                )
                return
        
        order.next_status()
        save_orders(self.orders)
        self.render_orders()
        
    def remove_order(self, order):
        """Función para eliminar la orden."""
        self.orders.remove(order)
        
        #Reiniciar el contador de ordenes si la lista queda vacia
        if not self.orders:
            Order.set_next_id(1)
        
        save_orders(self.orders)
        self.render_orders()

    def render_orders(self):
        """Dibuja todas las órdenes en el tablero."""
        for status_key in ORDER_STATUSES:
            container = self.tabs[status_key]
            for widget in container.winfo_children():
                widget.destroy()

            for i in range(ORDER_CARD_COLUMNS):
                container.columnconfigure(i, weight=1, uniform="col")

        positions = {status: 0 for status in ORDER_STATUSES}

        for order in self.orders:
            current_status_key = order.status.capitalize()
            frame = self.tabs[current_status_key]
            
            col = positions[current_status_key] % ORDER_CARD_COLUMNS
            row = positions[current_status_key] // ORDER_CARD_COLUMNS
            positions[current_status_key] += 1
            
            card = OrderCard(
                frame, 
                order, 
                self.elapsed_vars, 
                self.advance_order, 
                self.remove_order,
                self.open_edit_window,
                self.flashing_cards
            )
            card.grid(row=row, column=col, padx=10, pady=6, sticky="nsew")

        self.projection_manager.render()

    def _tick(self):
        """Actualiza el tiempo transcurrido en cada orden."""
        # Solo actualiza el tiempo si la ventana principal existe
        if self.root.winfo_exists():
            for order in self.orders:
                if order.number in self.elapsed_vars:
                    self.elapsed_vars[order.number].set(format_elapsed(order.created_at))
            
            #Manejar el parpadeo (pasamos la lista de tarjetas y órdenes)
            flash_modified_cards(self.root, self.orders, self.flashing_cards)

            #Cambia la frecuencia a 500ms para el parpadeo
            self.root.after(500, self._tick)
            
    def _start_tick(self):
        self._tick()
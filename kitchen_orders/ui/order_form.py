import tkinter as tk
from tkinter import messagebox
# Importar desde módulos locales
from ..models.order import Order
from ..config import MAX_PREPARING_ORDERS, FONTS, COLORS

class OrderForm(tk.Frame):
    def __init__(self, master, orders, render_orders_callback, open_projection_callback, notebook_widget, save_callback, **kwargs):
        super().__init__(master, padx=20, pady=20, **kwargs)
        self.orders = orders
        self.render_orders = render_orders_callback
        self.open_projection = open_projection_callback
        self.notebook = notebook_widget
        self.save_orders = save_callback
        self.pack(fill="both", expand=True)

        self._create_widgets()

    def _create_widgets(self):
        # Título
        tk.Label(self, text="Crear Nueva Orden",
                 font=FONTS["title"]).pack(pady=(0, 20))

        # Cliente
        tk.Label(self, text="Cliente:", font=FONTS["card_title"]).pack(anchor="w")
        self.table_entry = tk.Entry(self, font=FONTS["form"], width=40)
        self.table_entry.pack(pady=(5, 15), fill="x")

        # Productos
        tk.Label(self, text="Productos (uno por linea):", font=FONTS["card_title"]).pack(anchor="w")
        self.items_text = tk.Text(self, height=8, font=FONTS["form"], width=40)
        self.items_text.pack(pady=(5, 15), fill="both", expand=True)
        self.items_text.insert("1.0", "Ejemplo:\n1x Puerco\nx2 Res\n1x Chorizo")
        self.items_text.config(fg="gray")
        self.items_text.bind("<FocusIn>", self._clear_placeholder)

        # Notas
        tk.Label(self, text="Notas especiales (opcional):", font=FONTS["card_title"]).pack(anchor="w")
        self.notes_entry = tk.Entry(self, font=FONTS["form"], width=40)
        self.notes_entry.pack(pady=(5, 15), fill="x")

        # Botones
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Crear Orden", command=self._submit_order,
                  font=FONTS["button"], bg=COLORS["success_btn"], fg="white",
                  padx=20, pady=10).pack(side="left", padx=5)

        tk.Button(btn_frame, text="📺 Abrir Pantalla Carnicería",
                  command=self.open_projection,
                  font=FONTS["button"], bg=COLORS["projection_btn"], fg="white",
                  padx=20, pady=10).pack(side="left", padx=5)

    def _clear_placeholder(self, event):
        if self.items_text.get("1.0", "end-1c") == "Ejemplo:\n1x Puerco\nx2 Res\n1x Chorizo":
            self.items_text.delete("1.0", "end")
            self.items_text.config(fg="black")

    def _submit_order(self):
        table = self.table_entry.get().strip()
        items_raw = self.items_text.get("1.0", "end-1c").strip()
        notes = self.notes_entry.get().strip()

        if not table:
            messagebox.showwarning("Advertencia", "Por favor ingrese cliente")
            return
        if not items_raw or items_raw == "Ejemplo:\n1x Puerco\nx2 Res\n1x Chorizo":
            messagebox.showwarning("Advertencia", "Por favor ingresa al menos un producto")
            return

        items_list = [line.strip() for line in items_raw.split("\n") if line.strip()]

        new_order = Order(table, items_list, notes)
        self.orders.append(new_order)
        self.save_orders(self.orders)

        # Limpiar formulario
        self.table_entry.delete(0, "end")
        self.items_text.delete("1.0", "end")
        self.items_text.insert("1.0", "Ejemplo:\n1x Puerco\nx2 Res\n1x Chorizo")
        self.items_text.config(fg="gray")
        self.notes_entry.delete(0, "end")

        self.render_orders()
        self.notebook.select(1)
        messagebox.showinfo("Exito", f"Orden {new_order.number} creada correctamente")
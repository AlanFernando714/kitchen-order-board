import tkinter as tk
from tkinter import messagebox
# Importar desde módulos locales
from ..config import EDIT_WINDOW_SIZE, FONTS, COLORS

class EditWindow(tk.Toplevel):
    def __init__(self, master, order, save_edit_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.order = order
        self.save_edit_callback = save_edit_callback
        
        self.title(f"Editar Orden{order.number}")
        self.geometry(EDIT_WINDOW_SIZE)
        self.transient(master)
        self.grab_set()

        self._create_widgets()
        
    def _create_widgets(self):
        edit_frame = tk.Frame(self, padx=15, pady=15)
        edit_frame.pack(fill="both", expand=True)

        tk.Label(edit_frame, text=f"Edición de Orden{self.order.number}",
                 font=FONTS["title"]).pack(pady=(0, 15))

        # Cliente
        tk.Label(edit_frame, text="Cliente:", font=FONTS["card_title"]).pack(anchor="w")
        self.table_entry = tk.Entry(edit_frame, font=FONTS["form"], width=40)
        self.table_entry.insert(0, self.order.table)
        self.table_entry.pack(pady=(5, 10), fill="x")

        # Productos
        tk.Label(edit_frame, text="Productos (uno por linea):", font=FONTS["card_title"]).pack(anchor="w")
        self.items_text = tk.Text(edit_frame, height=8, font=FONTS["form"], width=40)
        self.items_text.insert("1.0", "\n".join(self.order.items))
        self.items_text.pack(pady=(5, 10), fill="both", expand=True)

        # Notas
        tk.Label(edit_frame, text="Notas especiales (opcional):", font=FONTS["card_title"]).pack(anchor="w")
        self.notes_entry = tk.Entry(edit_frame, font=FONTS["form"], width=40)
        self.notes_entry.insert(0, self.order.notes)
        self.notes_entry.pack(pady=(5, 15), fill="x")

        # Botones de acción
        btn_frame = tk.Frame(edit_frame)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Guardar Cambios",
                  command=self._save_changes,
                  font=FONTS["form"], bg=COLORS["save_edit_btn"], fg="white",
                  padx=10, pady=5).pack(side="left", padx=5)

        tk.Button(btn_frame, text="Cancelar", command=self.destroy,
                  font=FONTS["form"], padx=10, pady=5).pack(side="left", padx=5)

    def _save_changes(self):
        new_table = self.table_entry.get().strip()
        new_items_raw = self.items_text.get("1.0", "end-1c").strip()
        new_notes = self.notes_entry.get().strip()

        if not new_table or not new_items_raw:
            messagebox.showwarning("Advertencia", "Los campos Cliente y Productos no pueden estar vacíos", parent=self)
            return
        
        new_items_list = [line.strip() for line in new_items_raw.split("\n") if line.strip()]
        
        self.save_edit_callback(self, self.order, new_table, new_items_list, new_notes)
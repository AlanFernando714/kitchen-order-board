import tkinter as tk
from functools import partial
# Importar desde módulos locales
from ..utils.time_utils import format_elapsed
from ..config import FONTS, COLORS

class OrderCard(tk.Frame):
    def __init__(self, master, order, elapsed_vars, advance_callback, remove_callback, edit_callback, **kwargs):
        super().__init__(master, bd=2, relief="groove", padx=8, pady=6, width=250, bg=COLORS["ready_card"], **kwargs)
        self.order = order
        self.elapsed_vars = elapsed_vars
        self.advance_callback = advance_callback
        self.remove_callback = remove_callback
        self.edit_callback = edit_callback
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) 
        
        self._create_widgets()

    def _create_widgets(self):
        # Fila 0: Encabezado con tiempo
        header_frame = tk.Frame(self, bg=COLORS["ready_card"])
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        # Número de la orden y cliente
        tk.Label(header_frame, text=f"Order{self.order.number} - {self.order.table}",
                 font=FONTS["card_title"], bg=COLORS["ready_card"]).pack(side="left")

        # Tiempo transcurrido
        if self.order.number not in self.elapsed_vars:
            self.elapsed_vars[self.order.number] = tk.StringVar()
        tk.Label(header_frame, textvariable=self.elapsed_vars[self.order.number], 
                 fg="gray", bg=COLORS["ready_card"]).pack(side="right")
        
        # Fila 2: Items
        items_frame = tk.Frame(self, bg=COLORS["ready_card"])
        items_frame.grid(row=2, column=0, sticky="ew", pady=(0, 5))

        if len(self.order.items) > 5:
            items_frame.columnconfigure(0, weight=1)
            items_frame.columnconfigure(1, weight=1)
            for idx_item, item in enumerate(self.order.items):
                col_item = idx_item % 2
                row_item = idx_item // 2
                tk.Label(items_frame, text=f"• {item}", anchor="w", font=FONTS["card_item"], 
                         bg=COLORS["ready_card"]).grid(row=row_item, column=col_item, sticky="w", padx=2, pady=1)
        else:
            for item in self.order.items:
                tk.Label(items_frame, text=f"• {item}", anchor="w", font=FONTS["card_item"], 
                         bg=COLORS["ready_card"]).pack(fill="x")

        # Fila 3: Spacer
        tk.Frame(self, bg=COLORS["ready_card"]).grid(row=3, column=0, sticky="nsew")

        button_row = 5 
        
        if self.order.notes:
            notes_frame = tk.Frame(self, padx=6, pady=4, relief="solid", bg=COLORS["notes_bg"])
            notes_frame.grid(row=4, column=0, sticky="ew", pady=(0, 5))
            tk.Label(notes_frame, text=f"Nota: {self.order.notes}", fg=COLORS["notes_fg"],
                     font=FONTS["note_label"], bg=COLORS["notes_bg"],
                     wraplength=200, justify="left").pack(anchor="w", fill="x")
            button_row = 5 
        else:
            button_row = 4 

        # Fila del Botón
        button_frame = tk.Frame(self, bg=COLORS["ready_card"])
        button_frame.grid(row=button_row, column=0, sticky="ew", pady=(5, 0))

        # Botón Editar
        tk.Button(button_frame, text="Editar",
                  command=partial(self.edit_callback, self.order),
                  fg=COLORS["edit_btn_fg"], bd=0, bg=COLORS["ready_card"]).pack(side="left")

        # Botón de avance o eliminación
        if self.order.status == "Nuevo":
            btn_text = "Empezar a preparar"
            btn_color = COLORS["success_btn"]
            btn = tk.Button(button_frame, text=btn_text,
                            command=partial(self.advance_callback, self.order),
                            bg=btn_color, fg="white")
            btn.pack(side="right")
        elif self.order.status == "Preparando":
            btn_text = "Listo"
            btn_color = COLORS["ready_btn"]
            btn = tk.Button(button_frame, text=btn_text,
                            command=partial(self.advance_callback, self.order),
                            bg=btn_color, fg="white")
            btn.pack(side="right")
        else: # Ready
            btn = tk.Button(button_frame, text="Eliminar",
                            command=partial(self.remove_callback, self.order),
                            bg=COLORS["remove_btn"], fg="white")
            btn.pack(side="right")
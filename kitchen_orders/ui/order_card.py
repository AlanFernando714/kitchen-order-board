import tkinter as tk
from functools import partial
from datetime import datetime, timedelta
# Importar desde módulos locales
from ..utils.time_utils import format_elapsed
from ..config import FONTS, COLORS, MODIFIED_THRESHOLD

#Logica de modificacion reciente en tarjetas
def is_recently_modified(order):
    #Verificar si la orden fue modificada hace menos del umbral de tiempo
    #Asegurarse de que los campos existan.
    if not hasattr(order, 'updated_at') or not order.updated_at or not order.created_at:
        return False
    
    #La hora de actualizacion debe ser notablemente posterior a la de creacion
    is_modified = order.updated_at > order.created_at + timedelta(seconds=1)
    
    #La modificacion debe haber ocurrido dentro del umbral de 5 minutos
    is_recent= (datetime.now() - order.updated_at) < MODIFIED_THRESHOLD
    
    return is_modified and is_recent

"""
Widget personalizado (tk.Frame) que representa una única orden en el tablero.
Encargado de dibujar el contenido, el tiempo transcurrido y manejar las interacciones 
(avanzar estado, editar) y el resaltado visual de órdenes modificadas.
"""
class OrderCard(tk.Frame):
    def __init__(self, master, order, elapsed_vars, advance_callback, remove_callback, edit_callback, flashing_cards, **kwargs):
        
        self.order = order
        self.elapsed_vars = elapsed_vars
        self.advance_callback = advance_callback
        self.remove_callback = remove_callback
        self.edit_callback = edit_callback
        self.flashing_cards = flashing_cards
        
        is_modified = is_recently_modified(order)
        
        #Llamar a super().__init__ solo una vez al inicio, configurando el estilo final.
        if is_modified:
            #Estilo de alerta
            super().__init__(master, bd=0, relief="flat", padx=8, pady=6, width=250,
                             highlightbackground=COLORS["alert_color"],
                             highlightcolor=COLORS["alert_color"],
                             highlightthickness=4,
                             bg=COLORS["alert_bg"],
                             **kwargs)
            #Registrar la tarjeta para el parpadeo
            self.flashing_cards[order.number] = self
        else:
            #Estilo normal
            super().__init__(master, bd=2, relief="groove", padx=8, pady=6, width=250,
                             highlightthickness=4,
                             highlightbackground=COLORS["ready_card"],
                             highlightcolor=COLORS["ready_card"],
                             bg=COLORS["ready_card"],
                             **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) 
        
        self._create_widgets()

    def _create_widgets(self):
        #Obtener el color de fondo dinamico (amarillo o blanco)
        card_bg = self.cget("bg")
        
        # Fila 0: Encabezado con tiempo
        header_frame = tk.Frame(self, bg=card_bg)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        # Número de la orden y cliente
        tk.Label(header_frame, text=f"Order{self.order.number} - {self.order.table}",
                 font=FONTS["card_title"], bg=card_bg).pack(side="left")

        # Tiempo transcurrido
        if self.order.number not in self.elapsed_vars:
            self.elapsed_vars[self.order.number] = tk.StringVar()
        tk.Label(header_frame, textvariable=self.elapsed_vars[self.order.number], 
                 fg="gray", bg=card_bg, font=FONTS["time_main"]).pack(side="right")
        
        #Fila 1: Etiqueta de última edición
        if self.order.updated_at and self.order.updated_at> self.order.created_at + timedelta(seconds=1):
            updated_time_str= self.order.updated_at.strftime("%I:%M:%S %p")
            tk.Label(self,
                     text=f"Modificado: {updated_time_str}",
                     font=FONTS["note_label"],
                     fg="darkred",
                     bg=self.cget("bg") #Usar el color de fondo actual(alerta normal)
                    ).grid(row=1, column=0, sticky="w", padx=2,pady=0)
        # Fila 2: Items
        items_frame = tk.Frame(self, bg=card_bg) #Usar color de fondo de la tarjeta
        items_frame.grid(row=2, column=0, sticky="ew", pady=(0, 5))

        if len(self.order.items) > 5:
            items_frame.columnconfigure(0, weight=1)
            items_frame.columnconfigure(1, weight=1)
            for idx_item, item in enumerate(self.order.items):
                col_item = idx_item % 2
                row_item = idx_item // 2
                tk.Label(items_frame, text=f"• {item}", anchor="w", font=FONTS["card_item"], 
                         bg=card_bg).grid(row=row_item, column=col_item, sticky="w", padx=2, pady=1)
        else:
            for item in self.order.items:
                tk.Label(items_frame, text=f"• {item}", anchor="w", font=FONTS["card_item"], 
                         bg=card_bg).pack(fill="x")

        # Fila 3: Spacer
        tk.Frame(self, bg=card_bg).grid(row=3, column=0, sticky="nsew")

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
                  fg=COLORS["edit_btn_fg"], bd=0, bg=card_bg).pack(side="left")

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


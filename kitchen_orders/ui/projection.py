import tkinter as tk
from datetime import datetime, timedelta
# Importar desde módulos locales
from ..utils.time_utils import format_elapsed
from ..config import COLORS, FONTS, PROJECTION_WINDOW_SIZE, PROJECTION_COLUMNS, MAX_VISIBLE_PROJECTION_ORDERS, MODIFIED_THRESHOLD
from ..ui.order_card import is_recently_modified

class ProjectionWindow:
    def __init__(self, root, orders, elapsed_vars, **kwargs):
        self.root = root
        self.orders = orders
        self.elapsed_vars = elapsed_vars
        self.window = None
        self.projection_frame = None
        self.clock_var = tk.StringVar()
        self.flashing_projection_cards = {} #Rastrear tarjetas con alerta

    def open(self):
        if self.window is not None and self.window.winfo_exists():
            self.window.lift()
            self.window.focus_force()
            return

        self.window = tk.Toplevel(self.root)
        self.window.title("🔪 Carnicería - Órdenes en Preparación")
        self.window.geometry(PROJECTION_WINDOW_SIZE)
        self.window.state("zoomed")

        self._create_header()
        
        self.projection_frame = tk.Frame(self.window)
        self.projection_frame.pack(fill="both", expand=True)

        for i in range(PROJECTION_COLUMNS):
            self.projection_frame.columnconfigure(i, weight=1, uniform="col")
            
        self.render()
        self._start_alert_check() #Iniciar verificación de alertas

    def _create_header(self):
        header = tk.Frame(self.window, bg=COLORS["header_bg"], height=50)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        title_frame = tk.Frame(header, bg=COLORS["header_bg"])
        title_frame.pack(fill="x", pady=8)
        
        title_frame.columnconfigure(0, weight=1)
        title_frame.columnconfigure(1, weight=2)
        title_frame.columnconfigure(2, weight=1)
        
        tk.Label(title_frame, text="Órdenes en Preparación",
                 font=FONTS["header"], bg=COLORS["header_bg"], fg=COLORS["header_fg"]).grid(row=0, column=1, sticky="nsew")
        
        self.clock_label = tk.Label(title_frame, textvariable=self.clock_var,
                                     font=FONTS["clock"], bg=COLORS["header_bg"], fg=COLORS["clock_fg"])
        self.clock_label.grid(row=0, column=2, sticky="e", padx=20)
        
        self._update_clock()

    def _update_clock(self):
        self.clock_var.set(datetime.now().strftime("%H:%M:%S"))
        if self.window and self.window.winfo_exists():
            self.window.after(1000, self._update_clock)
            
            
    def _start_alert_check(self):
        #Inicia el ciclo de verificación de alertas en proyeccion
        if self.window and self.window.winfo_exists():
            self._check_modified_cards()
            self.window.after(500, self._start_alert_check)      
    
    def _check_modified_cards(self):
        #Verifica y actualiza el estilo de las tarjetas modificadas
        cards_to_remove = []
        
        for order_number, card in list(self.flashing_projection_cards.items()):
            order = next ((o for o in self.orders if o.number == order_number), None)
            
            #Si la orden no es reciente o no existe, restaurar estilo
            if not(order and is_recently_modified(order)):
                if card.winfo_exists():
                    #Restaurar el borde y el fondo general
                    card.config(
                        highlightcolor=COLORS["preparing_highlight"],
                        highlightbackground=COLORS["preparing_highlight"],
                        bg="white"
                    )
                    
                    #Restaurar bg de widgets hijos, sin eliminar texto de modificado
                    for child in card.winfo_children():
                        if isinstance(child, tk.Frame):
                            if child.cget("bg")== COLORS["alert_bg"]:
                                child.config(bg="white")
                            #Restaurar labels dentro de frames
                            for grandchild in child.winfo_children():
                                if isinstance(grandchild, tk.Label):
                                    current_bg = grandchild.cget("bg")
                                    if current_bg == COLORS["alert_bg"]:
                                        grandchild.config(bg="white")
                                    if "Modificado" in grandchild.cget("text"):
                                        grandchild.config(fg="darkred", bg=card.cget("bg"))
                cards_to_remove.append(order_number)
                
            #Limpiar tarjetas que ya no tienen alerta
            for order_number in cards_to_remove:
                del self.flashing_projection_cards[order_number]
            
    def render(self):
        if self.projection_frame is None or not self.projection_frame.winfo_exists():
            return

        for widget in self.projection_frame.winfo_children():
            widget.destroy()

        preparing_orders = [order for order in self.orders if order.status == "Preparando"]

        if not preparing_orders:
            tk.Label(self.projection_frame,
                     text="No hay órdenes en preparación",
                     font=FONTS["header"], fg="gray").grid(row=0, column=0, columnspan=PROJECTION_COLUMNS, pady=150)
            return

        for idx, order in enumerate(preparing_orders):
            if idx >= MAX_VISIBLE_PROJECTION_ORDERS:
                break
            
            col = idx % PROJECTION_COLUMNS
            row = idx // PROJECTION_COLUMNS
            
            #Determinar si la orden fue modificada recientemente
            is_modified = is_recently_modified(order)
            
            #Configurar colores segun si fue modificada
            card_bg = COLORS["alert_bg"] if is_modified else "white"
            border_color = COLORS["alert_color"] if is_modified else COLORS ["preparing_highlight"]
            border_width = 5 if is_modified else 3
            
            card = tk.Frame(self.projection_frame, bd=3, relief="solid",
                            padx=10, pady=8, bg=card_bg, highlightbackground=border_color,
                            highlightthickness=border_width)
            card.grid(row=row, column=col, padx=4, pady=12, sticky="nsew")

            #Registrar tarjeta si está modificada
            if is_modified:
                self.flashing_projection_cards[order.number] = card

            card.grid_columnconfigure(0, weight=1)
            card.grid_rowconfigure(1, weight=1)

            # Encabezado
            header_frame = tk.Frame(card, bg=COLORS["preparing_highlight"], padx=8, pady=5)
            header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
            
            tk.Label(header_frame, text=f"{order.number}",
                      font=FONTS["projection_order_num"], bg=COLORS["preparing_highlight"], fg=COLORS["header_fg"]).pack(side="left")
            
            tk.Label(header_frame, text=order.table,
                      font=FONTS["projection_table"], bg=COLORS["preparing_highlight"], fg=COLORS["header_fg"]).pack(side="left", padx=6)

            # Tiempo
            if order.number not in self.elapsed_vars:
                self.elapsed_vars[order.number] = tk.StringVar()
            
            tk.Label(header_frame, textvariable=self.elapsed_vars[order.number],
                      font=FONTS["projection_time"], bg=COLORS["preparing_highlight"], fg=COLORS["clock_fg"]).pack(side="right")
            
            #Mostrar etiqueta de modificacion si aplica
            if is_modified and order.updated_at:
                updated_time_str = order.updated_at.strftime("%I:%M:%S %p")
                mod_label_frame = tk.Frame(card, bg=card_bg)
                mod_label_frame.grid(row=1, column=0, sticky="ew", pady=(0,5))
                tk.Label(mod_label_frame, text=f"⚠️ Modificado: {updated_time_str}",
                         font=("Arial", 12, "bold"), bg=card_bg,
                         fg="darkred").pack(anchor="w", padx=5)
                items_row = 2
            else:
                items_row = 1
                         
            
            # Items
            items_frame = tk.Frame(card, bg=card_bg)
            items_frame.grid(row=items_row, column=0, sticky="ew", pady=(0, 5))
            
            if len(order.items) > 5:
                items_frame.columnconfigure(0, weight=1)
                items_frame.columnconfigure(1, weight=1)
                for idx_item, item in enumerate(order.items):
                    col_item = idx_item % 2
                    row_item = idx_item // 2
                    tk.Label(items_frame, text=f"• {item}", anchor="w", font=FONTS["projection_item_small"], 
                             bg="white").grid(row=row_item, column=col_item, sticky="w", pady=1, padx=1)
            else:
                for item in order.items:
                    tk.Label(items_frame, text=f"• {item}", anchor="w", font=FONTS["projection_item"], 
                             bg=card_bg).pack(fill="x", pady=1, padx=1)
            
            # Notas
            if order.notes:
                notes_frame = tk.Frame(card, bg=COLORS["notes_bg"], padx=6, pady=4, relief="solid", bd=1)
                notes_frame.grid(row=items_row+1, column=0, sticky="ew", pady=(5, 0))
                tk.Label(notes_frame, text=f"📝 {order.notes}",
                         font=FONTS["projection_note"], bg=COLORS["notes_bg"],
                         fg=COLORS["notes_fg"], wraplength=400, justify="left", anchor="w").pack(fill="x")
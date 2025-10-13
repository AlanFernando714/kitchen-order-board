# kitchen_orders/utils/time_utils.py

from datetime import datetime, timedelta
from .basic_time import format_elapsed
from ..config import COLORS, MODIFIED_THRESHOLD
from ..ui.order_card import is_recently_modified


#Recibir los datos de la instancia MainWindow para el parpadeo de las ediciones
def flash_modified_cards(root_widget, orders_lists, flashing_cards_dict):
    #Alterna el color del borde de las tarjetas recientemente modificadas
    
    #Se necesita un estado global para el parpadeo, se define como un atributo del widget root
    if not hasattr(root_widget, '_flash_state'):
        root_widget._flash_state = True
    
    root_widget._flash_state = not root_widget._flash_state
    
    color_alert = COLORS["alert_color"]
    color_normal = COLORS["flash_color_alt"]
    
    current_color = color_alert if root_widget._flash_state else color_normal
    
    cards_to_remove = []
    
    for order_number, card in list(flashing_cards_dict.items()):
        order = next ((o for o in orders_lists if o.number == order_number), None)
        
        #Verificar si la tarjeta aún debe parpadear
        if order and is_recently_modified(order):
            if card.winfo_exists():
                # Durante el parpadeo, cambiar highlightcolor y highlightbackground
                # para que el borde completo parpadee
                # Solo actualizar si el color ha cambiado
                last_color = root_widget._last_card_colors.get(order_number)
                if last_color != current_color:
                    card.config(
                        highlightcolor=current_color,
                        highlightbackground=current_color,
                        highlightthickness=4
                    )
                    root_widget._last_card_colors[order_number] = current_color
        else:
            #Restaurar estilo normal al expirar o si la orden fue eliminada
            if card.winfo_exists():
                card.config(
                    highlightcolor="SystemButtonFace",
                    highlightbackground="SystemButtonFace",
                    highlightthickness=0,
                    bd=2,
                    relief="groove",
                    bg=COLORS["ready_card"]
                )
            #Limpiar del diccionario de colores
            if order_number in root_widget._last_card_colors:
                del root_widget._last_card_colors[order_number]
            cards_to_remove.append(order_number)
    
    #Remover tarjetas que ya no deben parpadear
    for order_number in cards_to_remove:
        del flashing_cards_dict[order_number]
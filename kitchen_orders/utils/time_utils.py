# kitchen_orders/utils/time_utils.py

from datetime import datetime, timedelta
from .basic_time import format_elapsed
from ..config import COLORS, MODIFIED_THRESHOLD
from ..ui.order_card import is_recently_modified


#Recibir los datos de la instancia MainWindow para el parpadeo de las ediciones
def flash_modified_cards(root_widget, orders_lists, flashing_cards_dict):
    #Alterna el color del borde de las tarjetas recientemente modificadas
    
    color_alert = COLORS["alert_color"]
     
    cards_to_remove = []
    
    for order_number, card in list(flashing_cards_dict.items()):
        order = next ((o for o in orders_lists if o.number == order_number), None)
        
        #Verificar si la tarjeta aún debe parpadear
        if order and is_recently_modified(order):
             #La tarjeta mantiene su estilo de alerta
             pass
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
            cards_to_remove.append(order_number)
    
    #Remover tarjetas que ya no deben parpadear
    for order_number in cards_to_remove:
        del flashing_cards_dict[order_number]
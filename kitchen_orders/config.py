# kitchen_orders/config.py
"""Configuraciones generales de la aplicación"""

#Timedelta para definir umbral de tiempo
from datetime import timedelta

# Archivos y rutas
BACKUP_FILE = "orders_backup.json"

#Umbral de tiempo para la alerta de modificacion de la órden
MODIFIED_THRESHOLD = timedelta(minutes=1) #El tiempo que dura el parpadeo de la tarjeta

# Configuración de ventanas
MAIN_WINDOW_SIZE = "800x600"
PROJECTION_WINDOW_SIZE = "1920x1080+1366+0" # Ajusta a tu configuración de monitor/TV
EDIT_WINDOW_SIZE = "450x550"

# Límites de órdenes
MAX_PREPARING_ORDERS = 15
MAX_VISIBLE_PROJECTION_ORDERS = 15

# Configuración de UI
PROJECTION_COLUMNS = 5
ORDER_CARD_COLUMNS = 5

# Estados de órdenes
ORDER_STATUSES = ["Nuevo", "Preparando", "Listo"]

# Colores (Se puede cambiar diseño de la aplicacion)
COLORS = {
    "header_bg": "#2c3e50",
    "header_fg": "white",
    "clock_fg": "#ffeb3b",
    "preparing_highlight": "#3498db",
    "notes_bg": "#fff3cd",
    "notes_fg": "#f57f17",
    "success_btn": "#4CAF50",
    "projection_btn": "#3498db",
    "ready_btn": "#f39c12",
    "remove_btn": "#e74c3c",
    "edit_btn_fg": "#2980b9",
    "save_edit_btn": "#2ecc71",
    "ready_card": "white",
    "alert_color": "#FF9800", 
    "flash_color_alt": "#E0E0E0",
    "alert_bg": "#FFFDE7"
}

# Fuentes
FONTS = {
    "title": ("Arial", 16, "bold"),
    "header": ("Arial", 20, "bold"),
    "clock": ("Arial", 20, "bold"),
    "time_main": ("Arial",7),
    "card_title": ("Arial", 11, "bold"),
    "card_item": ("Arial", 11),
    "projection_order_num": ("Arial", 14, "bold"),
    "projection_table": ("Arial", 15),
    "projection_time": ("Arial", 11),
    "projection_item": ("Arial", 18, "bold"),
    "projection_item_small": ("Arial", 15, "bold"),
    "projection_note": ("Arial", 13, "italic"),
    "projection_modified": ("Arial", 12, "bold"),
    "projection_modified_old": ("Arial", 11, "normal"),
    "button": ("Arial", 12, "bold"),
    "form": ("Arial", 11),
    "note_label": ("Arial", 10)
}
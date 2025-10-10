# kitchen_orders/ui/__init__.py

from .main_window import MainWindow
from .order_form import OrderForm
from .order_card import OrderCard
from .edit_window import EditWindow
from .projection import ProjectionWindow

# Esto permite que otros módulos importen la ventana principal de forma concisa:
# from .ui import MainWindow 
# Por ejemplo, en el archivo principal (main.py):
# from .ui import MainWindow
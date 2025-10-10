# kitchen_orders/data/__init__.py

from .storage import save_orders, load_orders

# Ahora, en main_window.py, puedes hacer:
# from ..data import save_orders, load_orders
# en lugar de:
# from ..data.storage import save_orders, load_orders
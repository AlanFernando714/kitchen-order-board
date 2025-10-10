# kitchen_orders/models/__init__.py

from .order import Order

# Esto permite que la clase Order sea importada directamente usando:
# from ..models import Order 
# en lugar de la ruta más larga:
# from ..models.order import Order
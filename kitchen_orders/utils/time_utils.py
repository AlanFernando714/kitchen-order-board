# kitchen_orders/utils/time_utils.py

from datetime import datetime

def format_elapsed(created_at):
    """
    Calcula y formatea el tiempo transcurrido desde la creación de la orden.
    Retorna un string legible (e.g., 'Tiempo: 5m 30s').
    """
    # Calcula la diferencia entre el tiempo actual y el tiempo de creación
    diff = datetime.now() - created_at
    total_seconds = int(diff.total_seconds())
    
    # Usa divmod para dividir y obtener el residuo de forma eficiente
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    
    # Formatea el resultado
    if hours > 0:
        return f"Tiempo: {hours}h {minutes}m"
    elif minutes > 0:
        return f"Tiempo: {minutes}m {seconds}s"
    else:
        return f"Tiempo: {seconds}s"
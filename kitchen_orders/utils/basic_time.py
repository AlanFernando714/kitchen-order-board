from datetime import datetime

def format_elapsed(created_at):
    #Calcula y formatea el tiempo transcurrido desde la creación de la orden.
    
    diff = datetime.now() - created_at
    total_seconds = int(diff.total_seconds())
    
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    
    if hours > 0:
        return f"Tiempo: {hours}h {minutes}m"
    elif minutes> 0:
        return f"Tiempo: {minutes}m {seconds}s"
    else:
        return f"Tiempo:{seconds}s"
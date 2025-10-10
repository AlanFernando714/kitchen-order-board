# kitchen_orders/main.py

import tkinter as tk
# Importar desde el paquete modularizado
from .data.storage import load_orders
from .ui.main_window import MainWindow

if __name__ == "__main__":
    # 1. Cargar la lista de órdenes (desde JSON o crea ejemplos)
    orders = load_orders()
    
    # 2. Configuración de la ventana raíz de Tkinter
    root = tk.Tk()
    
    # 3. Crear e inicializar la aplicación principal (toda la UI)
    app = MainWindow(root, orders)
    
    # 4. Ejecutar el loop principal de la interfaz gráfica
    root.mainloop()

# NOTA: La lógica de la aplicación está encapsulada en MainWindow,
# lo que mantiene main.py simple y centrado en el inicio.
import tkinter as tk
from .data.storage import load_orders
from .ui.main_window import MainWindow

#Funcion para ejecutar directamente desde run.py
def main():
    orders = load_orders()
    root = tk.Tk()
    app = MainWindow(root, orders)
    root.mainloop()

if __name__ == "__main__":
    main()
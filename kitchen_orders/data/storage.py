# kitchen_orders/data/storage.py

import json
import os
import sys
from ..models.order import Order # Importa la clase Order


def get_backup_path():
    #Obtiene la ruta correcta del archivo de backup, funciona en desarrollo y en ejecutable
    #Al crear ejecutable, su archivo backup se crera en la carpeta: C:\Users\<tu_usuario>\AppData\Roaming\KitchenOrders\orders_backup.json
    if getattr(sys, 'frozen', False):
        #Ejecutable empaquetado con PyInstaller
        appdata_dir = os.path.join(os.getenv("APPDATA"), "KitchenOrders")
        os.makedirs(appdata_dir, exist_ok=True)
        backup_file = os.path.join(appdata_dir, "orders_backup.json")
    else:
        #En desarrollo
        #Archivo backup se guarda en carpeta raiz del proyecto.
        app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        backup_file = os.path.join(app_dir, "orders_backup.json")
    return backup_file

def save_orders(orders):
    """Guarda la lista de órdenes y el último ID asignado en un archivo JSON."""
    try:
        backup_path = get_backup_path()
        
        data = {
            "last_id": Order._ids,
            "orders": [order.to_dict() for order in orders]
        }
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Backup guardado en: {backup_path}")
    except Exception as e:
        print(f"Error al guardar bacjup: {e}")

def load_orders():
    """Carga la lista de órdenes desde un archivo JSON o crea ejemplos si no existe."""
    backup_path = get_backup_path()
    
    if os.path.exists(backup_path):
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
            orders_list = [Order.from_dict(order_data) for order_data in data.get("orders",[])]
            
            if not orders_list:
                Order.set_next_id(1)
            else:
                Order.set_next_id(data.get("last_id", 1))
                
            print(f"Backup cargado desde: {backup_path}")
            print(f"Órdenes restauradas: {len(orders_list)}")
            return orders_list
        
        except Exception as e:
            print(f"Error al cargar backup: {e}")
            return []
    else:
        print(f"No se encontró archivo de backup en: {backup_path}")
        print("Creando órdenes de ejemplo.")         
         
        #Para eliminar el ejemplo de órdenes, únicamente dejar orders_list = []
        orders_list = [
            Order("Cliente 1", ["5kg Res taco", "9kg Res guiso"]),
            Order("Cliente 2", ["2kg Higado", "3kg Molida", "2kg Jamon", "3kg Chorizo", "5kg Manitas"], "Para las 2pm"),
            Order("Cliente 3", ["1kg Puerco", "2kg Pollo"])
        ]
        return orders_list
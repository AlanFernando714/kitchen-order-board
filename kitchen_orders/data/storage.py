# kitchen_orders/data/storage.py

import json
import os
from ..models.order import Order # Importa la clase Order
from ..config import BACKUP_FILE # Importa el nombre del archivo de backup

def save_orders(orders):
    """Guarda la lista de órdenes y el último ID asignado en un archivo JSON."""
    try:
        # Usa Order._ids para guardar el próximo ID que debería asignarse
        data = {
            "last_id": Order._ids,
            "orders": [order.to_dict() for order in orders]
        }
        with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
            # 'ensure_ascii=False' permite guardar caracteres especiales como la ñ o tildes
            json.dump(data, f, ensure_ascii=False, indent=2) 
        print(f"Backup guardado: {len(orders)} órdenes")
    except Exception as e:
        print(f"Error al guardar backup: {e}")

def load_orders():
    """Carga la lista de órdenes desde un archivo JSON o crea ejemplos si no existe."""
    if os.path.exists(BACKUP_FILE):
        try:
            with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 1. Restaurar el contador de IDs en la clase Order
            # La función set_next_id la definimos en models/order.py
            Order.set_next_id(data.get("last_id", 1))

            # 2. Restaurar las órdenes, usando el método estático from_dict
            orders_list = [Order.from_dict(order_data) for order_data in data.get("orders", [])]
            print(f"Backup cargado: {len(orders_list)} órdenes restauradas")
            return orders_list

        except Exception as e:
            print(f"Error al cargar backup: {e}")
            return [] # Retorna lista vacía en caso de error

    else:
        # Si no existe archivo, crea órdenes de ejemplo
        print("No se encontró archivo de backup. Creando órdenes de ejemplo.")
        orders_list = [
            Order("Cliente 1", ["5kg Res taco", "9kg Res guiso"]),
            Order("Cliente 2", ["2kg Higado", "3kg Molida", "2kg Jamon", "3kg Chorizo", "5kg Manitas"], "Para las 2pm"),
            Order("Cliente 3", ["1kg Puerco", "2kg Pollo"])
        ]
        return orders_list
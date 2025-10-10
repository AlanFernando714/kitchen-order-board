# kitchen_orders/models/order.py

from datetime import datetime

class Order:
    # Variable de clase para llevar la cuenta del próximo ID a asignar
    _ids = 1  
    
    def __init__(self, table, items, notes="", status="Nuevo", created_at=None, number=None):
        """
        Constructor de la clase Order.
        Inicializa una nueva orden o restaura una existente desde datos cargados.
        """
        if number:
            self.number = number
            # Al restaurar, nos aseguramos de que el contador de IDs no retroceda
            try:
                num_int = int(number.lstrip('#'))
                if num_int >= Order._ids:
                    Order._ids = num_int + 1
            except ValueError:
                pass 
        else:
            # Asigna un nuevo número de orden en formato: #001, #002...
            self.number = f"#{Order._ids:03d}"
            Order._ids += 1

        self.table = table
        self.items = items
        self.notes = notes
        self.status = status

        if created_at:
            # Si se carga desde archivo (es un string ISO), lo convierte a datetime
            if isinstance(created_at, str):
                self.created_at = datetime.fromisoformat(created_at)
            else:
                self.created_at = created_at
        else:
            # Para órdenes nuevas, registra la hora actual
            self.created_at = datetime.now()

    def next_status(self):
        """Avanza el estado de la orden (Nuevo -> Preparando -> Listo)."""
        if self.status == "Nuevo":
            self.status = "Preparando"
        elif self.status == "Preparando":
            self.status = "Listo"

    def to_dict(self):
        """Convierte el objeto Order a un diccionario (para guardar en JSON)."""
        return {
            "number": self.number,
            "table": self.table,
            "items": self.items,
            "notes": self.notes,
            "status": self.status,
            # Usa isoformat() para serializar datetime de forma segura
            "created_at": self.created_at.isoformat() 
        }

    @staticmethod
    def from_dict(data):
        """Método estático para crear un objeto Order desde un diccionario cargado (JSON)."""
        return Order(
            table=data["table"],
            items=data["items"],
            notes=data.get("notes", ""),
            status=data.get("status", "Nuevo"),
            created_at=data.get("created_at"),
            number=data.get("number")
        )

    @classmethod
    def set_next_id(cls, last_id):
        """Método de clase para restaurar el contador de IDs desde el backup."""
        # Asegura que el próximo ID a asignar sea el último ID guardado
        cls._ids = last_id
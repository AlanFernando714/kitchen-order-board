
# 🍴 Kitchen Orders - Sistema de Gestión de Órdenes

Sistema de gestión de órdenes para carnicería/cocina con interfaz gráfica desarrollado en Python usando Tkinter.

---

## 📋 Características
- ✨ Interfaz gráfica intuitiva con pestañas
- 📝 Creación rápida de órdenes con cliente, productos y notas
- 🔄 Gestión de estados: New → Preparing → Ready
- ⏱️ Temporizador en tiempo real para cada orden
- 📺 Ventana de proyección para pantalla secundaria/TV
- ✏️ Edición de órdenes existentes
- 💾 Guardado automático en JSON (backup persistente)
- 🎨 Diseño responsive con scroll automático

---

## 🚀 Instalación

### Requisitos
- Python 3.7 o superior
- Tkinter (generalmente incluido con Python)

### Instalación rápida
```bash
# Clonar el repositorio
git clone https://github.com/AlanFernando714/kitchen-order-board.git
cd kitchen-order-board

# Ejecutar la aplicación
python main.py
```

---

## 📁 Estructura del Proyecto
```
kitchen_orders/
│
├── main.py
├── config.py
├── models/
│   ├── __init__.py
│   └── order.py
├── data/
│   ├── __init__.py
│   └── storage.py
├── ui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── order_form.py
│   ├── order_card.py
│   ├── projection.py
│   └── edit_window.py
├── utils/
│   ├── __init__.py
│   └── time_utils.py
├── orders_backup.json
└── README.md
```

---

## 🎯 Uso

### Crear una nueva orden
1. Ve a la pestaña "+ Nueva Orden"
2. Ingresa el nombre del cliente
3. Agrega los productos (uno por línea)
4. Opcionalmente, agrega notas especiales
5. Haz clic en "Crear Orden"

### Gestionar órdenes
- **New**: Órdenes recién creadas  
- Ckick en "Editar" → Permite editar el contenido de la orden
- Click en "Empezar a preparar" → **Preparando**  
- Click en "Listo" → **Listo**  
- Click en "Eliminar" → Elimina la orden

### Ventana de Proyección
- Haz clic en "📺 Abrir Pantalla Carnicería"
- Muestra hasta 15 órdenes simultáneamente
- Actualización en tiempo real
- Diseño optimizado para visualización a distancia

---

## ⚙️ Configuración
Editar `config.py` para personalizar:
- Límite de órdenes en preparación
- Tamaños de ventana
- Colores y fuentes
- Número de columnas en las cuadrículas

---

## 💾 Persistencia de Datos
- Datos guardados automáticamente en `orders_backup.json`
- Backup actualizado al crear, cambiar estado, editar o eliminar órdenes

---

## 📝 Licencia
Este proyecto está bajo la licencia **MIT**.

---

## 👨‍💻 Autor
**Alan Fernando Carlos Flores**  
Desarrollado para optimizar la gestión de órdenes en carnicerías y cocinas.

📧 Contacto: alan.carlos.f2004@gmail.com  
🔗 GitHub: [AlanFernando714](https://github.com/AlanFernando714)

---

## 🐛 Reporte de Bugs
Si encuentras un bug, abre un issue en GitHub indicando:
1. Descripción del problema
2. Pasos para reproducirlo
3. Comportamiento esperado vs actual
4. Screenshots si es posible

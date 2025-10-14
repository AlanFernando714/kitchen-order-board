🍴 Kitchen Orders - Sistema de Gestión de Órdenes
Sistema de gestión de órdenes para carnicería/cocina con interfaz gráfica desarrollado en Python usando Tkinter.

📋 Características
✨ Interfaz gráfica intuitiva con pestañas
📝 Creación rápida de órdenes con cliente, productos y notas
🔄 Gestión de estados: Nuevo → Preparando → Listo
⏱️ Temporizador en tiempo real para cada orden
📺 Ventana de proyección para pantalla secundaria/TV
✏️ Edición de órdenes existentes
🔔 Resaltado visual de órdenes editadas (borde naranja durante 5 minutos)
⚠️ Alertas en pantalla de proyección para órdenes modificadas
💾 Guardado automático en JSON (backup persistente)
🎨 Diseño responsive con scroll automático

🚀 Instalación
Requisitos
Python 3.7 o superior
Tkinter (generalmente incluido con Python)
Instalación rápida
bash

# Clonar el repositorio
git clone https://github.com/AlanFernando714/kitchen-order-board.git
cd kitchen-order-board

# Ejecutar la aplicación
python main.py

📁 Estructura del Proyecto
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
│   ├── basic_time.py
│   └── time_utils.py
├── orders_backup.json
└── README.md

🎯 Uso
Crear una nueva orden
Ve a la pestaña "+ Nueva Orden"
Ingresa el nombre del cliente
Agrega los productos (uno por línea)
Opcionalmente, agrega notas especiales
Haz clic en "Crear Orden"

Gestionar órdenes
Nuevo: Órdenes recién creadas
Click en "Editar" → Permite editar el contenido de la orden
Las órdenes editadas se destacan con borde naranja durante 5 minutos
Se muestra la hora de última modificación
El resaltado aparece tanto en la ventana principal como en la proyección
Click en "Empezar a preparar" → Mueve a Preparando
Click en "Listo" → Mueve a Listo
Click en "Eliminar" → Elimina la orden

Sistema de alertas visuales
Cuando editas una orden:

🟠 Borde naranja rodea la tarjeta
📝 Etiqueta "Modificado: [hora]" visible
⏲️ Duración: 5 minutos (configurable en config.py)
📺 Visible en ambas pantallas (principal y proyección)
🔄 Se restaura automáticamente al estilo normal después del tiempo establecido

Nota:
Órdenes de ejemplo creadas en la pestaña "Nuevo", puedes eliminarlas editando el archivo storage.py

Ventana de Proyección
Haz clic en "📺 Abrir Pantalla Carnicería"
Muestra hasta 15 órdenes simultáneamente
Actualización en tiempo real
Diseño optimizado para visualización a distancia
Resalta órdenes modificadas con advertencia visual ⚠️

⚙️ Configuración
Editar config.py para personalizar:

Límite de órdenes en preparación
Tiempo de resaltado de ediciones (MODIFIED_THRESHOLD)
Tamaños de ventana
Colores y fuentes (incluyendo alert_color y alert_bg)
Número de columnas en las cuadrículas

Ejemplo de configuración de alertas
python

# En config.py
MODIFIED_THRESHOLD = timedelta(minutes=5)  # Duración del resaltado

COLORS = {
    "alert_color": "#FF9800",      # Color del borde (naranja)
    "alert_bg": "#FFFDE7",         # Color de fondo (amarillo claro)
    # ... otros colores
}

💾 Persistencia de Datos
Datos guardados automáticamente en orders_backup.json
Backup actualizado al crear, cambiar estado, editar o eliminar órdenes
Se preserva la marca de tiempo de edición para el sistema de alertas
Estructura del archivo JSON
json
{
  "last_id": 4,
  "orders": [
    {
      "number": "#001",
      "table": "Cliente 1",
      "items": ["5kg Res taco", "9kg Res guiso"],
      "notes": "",
      "status": "Nuevo",
      "created_at": "2025-01-15T10:30:00",
      "updated_at": "2025-01-15T10:35:00"
    }
  ]
}

🎨 Características Visuales
Tarjetas de Órdenes
Estado normal: Borde gris sutil
Orden editada: Borde naranja grueso + fondo amarillo claro
Información del tiempo transcurrido
Hora de última modificación cuando aplica
Pantalla de Proyección
Diseño de alta visibilidad
Alertas destacadas para órdenes modificadas
Reloj en tiempo real
Distribución en columnas optimizada

📝 Licencia
Este proyecto está bajo la licencia MIT.

👨‍💻 Autor
Alan Fernando Carlos Flores
Desarrollado para optimizar la gestión de órdenes en carnicerías y cocinas.

📧 Contacto: alan.carlos.f2004@gmail.com
🔗 GitHub: AlanFernando714

🐛 Reporte de Bugs
Si encuentras un bug, abre un issue en GitHub indicando:

Descripción del problema
Pasos para reproducirlo
Comportamiento esperado vs actual
Screenshots si es posible

🔄 Changelog
v2.0 - Sistema de Alertas de Edición
✨ Resaltado visual de órdenes editadas (5 minutos)
📺 Alertas en pantalla de proyección
🕒 Registro de marca de tiempo de última modificación
🎨 Mejoras en la experiencia visual

v1.0 - Versión Inicial
Sistema básico de gestión de órdenes
Ventana de proyección
Persistencia de datos

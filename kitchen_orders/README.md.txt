Kitchen Orders - Sistema de Gestión de Órdenes
Sistema de gestión de órdenes para carnicería/cocina con interfaz gráfica desarrollado en Python usando Tkinter.

📋 Características
✨ Interfaz gráfica intuitiva con pestañas
📝 Creación rápida de órdenes con cliente, productos y notas
🔄 Gestión de estados: New → Preparing → Ready
⏱️ Temporizador en tiempo real para cada orden
📺 Ventana de proyección para pantalla secundaria/TV
✏️ Edición de órdenes existentes
💾 Guardado automático en JSON (backup persistente)
🎨 Diseño responsive con scroll automático
🚀 Instalación
Requisitos
Python 3.7 o superior
Tkinter (generalmente incluido con Python)
Instalación rápida
bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/kitchen-orders.git
cd kitchen-orders

# Ejecutar la aplicación
python main.py
📁 Estructura del Proyecto
kitchen_orders/
│
├── main.py                 # Punto de entrada principal
├── config.py              # Configuraciones generales
│
├── models/
│   ├── __init__.py
│   └── order.py           # Clase Order (modelo de datos)
│
├── data/
│   ├── __init__.py
│   └── storage.py         # Guardado/carga en JSON
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py     # Ventana principal y pestañas
│   ├── order_form.py      # Formulario de nueva orden
│   ├── order_card.py      # Renderizado de tarjetas
│   ├── projection.py      # Ventana de proyección
│   └── edit_window.py     # Ventana de edición
│
├── utils/
│   ├── __init__.py
│   └── time_utils.py      # Utilidades de formato de tiempo
│
├── orders_backup.json     # Archivo de backup (se crea automáticamente)
└── README.md              # Este archivo
🎯 Uso
Crear una nueva orden
Ve a la pestaña "+ Nueva Orden"
Ingresa el nombre del cliente
Agrega los productos (uno por línea)
Opcionalmente, agrega notas especiales
Haz clic en "Crear Orden"
Gestionar órdenes
New: Órdenes recién creadas
Click en "Start Cooking" para mover a Preparing
Preparing: Órdenes en preparación
Click en "Mark Ready" cuando estén listas
Ready: Órdenes completadas
Click en "Remove" para eliminar
Ventana de Proyección
Haz clic en "📺 Abrir Pantalla Carnicería" para mostrar todas las órdenes en preparación en una pantalla secundaria o TV.

Muestra hasta 15 órdenes simultáneamente
Actualización en tiempo real
Diseño optimizado para visualización a distancia
Reloj en tiempo real
⚙️ Configuración
Puedes personalizar la aplicación editando config.py:

Límite de órdenes en preparación
Tamaños de ventana
Colores y fuentes
Número de columnas en las cuadrículas
💾 Persistencia de Datos
Los datos se guardan automáticamente en orders_backup.json
El backup se actualiza cada vez que:
Se crea una orden
Se cambia el estado de una orden
Se edita una orden
Se elimina una orden
🤝 Contribuciones
Las contribuciones son bienvenidas. Por favor:

Fork el proyecto
Crea una rama para tu feature (git checkout -b feature/AmazingFeature)
Commit tus cambios (git commit -m 'Add some AmazingFeature')
Push a la rama (git push origin feature/AmazingFeature)
Abre un Pull Request
📝 Licencia
Este proyecto es de código abierto y está disponible bajo la licencia MIT.

👨‍💻 Autor
Desarrollado con ❤️ para optimizar la gestión de órdenes en carnicerías y cocinas.

🐛 Reporte de Bugs
Si encuentras un bug, por favor abre un issue en GitHub con:

Descripción del problema
Pasos para reproducirlo
Comportamiento esperado vs actual
Screenshots si es posible
📧 Contacto
Para preguntas o sugerencias, abre un issue en GitHub.


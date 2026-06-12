# Aplicaciones del Robot

Esta carpeta contiene scripts y nodos de ROS 2 que implementan la lógica de alto nivel, control y pruebas del robot.

## Herramientas de Control

### 🎮 `control_teclado_trapezoidal.py`
La herramienta principal de teleoperación. Permite mover el robot usando el teclado con perfiles de velocidad trapezoidales para movimientos suaves.

*   **Uso**: `ros2 run can_comm_pkg control_teclado`
*   **Teclas**:
    *   `1-5` / `Q-T`: Mover articulaciones J1-J5 (+/-).
    *   `M`: Cambiar modo (Joint/Cartesian/Camera).
    *   `R`: Grabar trayectoria.
    *   `P`: Reproducir trayectoria.

### 📈 `can_traj.py`
Interfaz gráfica (GUI) basada en Tkinter para generar y ejecutar trayectorias complejas.
*   Permite guardar puntos (waypoints).
*   Genera interpolación LSPB (Linear Segment with Parabolic Blend).
*   Visualiza la trayectoria antes de ejecutarla.

### 👁️ `product_identifier.py`
Sistema de visión artificial.
*   Usa la cámara en la muñeca para detectar códigos de barras o productos.
*   Publica los objetos detectados en tópicos ROS.

## Scripts de Prueba (`test/`)

Scripts para validar el funcionamiento de cada articulación individualmente.

*   `jX_step_test.py`: Respuesta al escalón.
*   `jX_ramp_test.py`: Seguimiento de rampa.

## Utilidades

*   `ik_node.py`: Servicio de Cinemática Inversa.
*   `cli_node.py`: Interfaz de línea de comandos para enviar comandos CAN directos.
*   `visualize_dh.py`: Visualizador de parámetros Denavit-Hartenberg.

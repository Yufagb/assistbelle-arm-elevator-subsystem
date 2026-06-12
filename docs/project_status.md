# Estado actual del proyecto HardwareX

Este documento resume el estado real de la rama `hardwarex-publication-package`.

## Resumen ejecutivo

La rama ya tiene una estructura ordenada para publicacion, firmware ESP32 migrado y documentacion tecnica inicial. El repositorio separa correctamente ROS 2, firmware, electronica, hardware mecanico, validacion y manuscrito.

El firmware ESP32 J1-J5 compila localmente. ROS 2 tambien compila localmente para el paquete `can_comm_pkg`. El nodo `can_node` inicia correctamente usando una interfaz `can0` virtual creada con SocketCAN/vcan.

La BOM inicial ya fue completada desde la hoja de Drive `Lista de Materiales` y se agregaron precios referenciales cuando el costo registrado era 0 o institucional. El siguiente bloque critico es completar evidencias fisicas y documentales: CAD, diagramas finales, fotos y datasets curados.

## Estado por area

| Area | Estado | Observacion |
|---|---|---|
| Estructura del repo | Avanzada | Definida en `docs/repository_structure.md`. |
| Firmware J1 | Compila localmente | Proyecto ESP-IDF en `firmware/esp32_joint_node/J1`. |
| Firmware J2 | Compila localmente | Proyecto ESP-IDF en `firmware/esp32_joint_node/J2`. |
| Firmware J3 | Compila localmente | Proyecto ESP-IDF en `firmware/esp32_joint_node/J3`. |
| Firmware J4 | Compila localmente | Incluye gripper en GPIO4. |
| Firmware J5 | Compila localmente | Proyecto ESP-IDF en `firmware/esp32_stepper_node/J5_tb6600`. |
| Pinout ESP32 | Documentado | Ver `electronics/pinout_tables/esp32_pinout_table.md`. |
| Raspberry Pi/MCP2515 | Documentado | Ver `electronics/pinout_tables/raspberry_pi_mcp2515.md`. |
| Bus principal | Documentado parcialmente | Falta diagrama final en imagen/PDF. |
| Protocolo CAN | Documentado | Ver `firmware/can_protocol/can_messages.md`. |
| ROS 2 | Compila e inicia con vcan | `can_comm_pkg` compila y `can_node` inicia con `can0` virtual. |
| BOM | Inicial completa | Ver `docs/bom_template.csv`; faltan costos finales de algunos componentes institucionales. |
| CAD/STEP/STL | Pendiente | Todavia no se cuenta con CAD completo. |
| Validacion | Pendiente de curado | Mover evidencias limpias desde `resultados/` hacia `validation/`. |
| Paper | Pendiente | Carpeta creada, falta manuscrito. |

## Firmware ESP32 validado

El firmware se organiza asi:

```text
firmware/
├── esp32_joint_node/
│   ├── J1/
│   ├── J2/
│   ├── J3/
│   └── J4/
└── esp32_stepper_node/
    └── J5_tb6600/
```

Cada nodo tiene estructura ESP-IDF con `CMakeLists.txt`, `sdkconfig` y carpeta `main/`.

## Pinout principal

| Nodo | Subsistema | CAN TX | CAN RX | Actuacion | Encoder / extra |
|---|---|---:|---:|---|---|
| J1 | Base | GPIO21 | GPIO22 | IN1 GPIO32, IN2 GPIO33 | A GPIO10, B GPIO13 |
| J2 | Hombro | GPIO22 | GPIO21 | IN1 GPIO5, IN2 GPIO17 | A GPIO19, B GPIO18 |
| J3 | Codo | GPIO21 | GPIO22 | IN1 GPIO32, IN2 GPIO33 | A GPIO10, B GPIO13 |
| J4 | Muneca + gripper | GPIO33 | GPIO32 | IN1 GPIO25, IN2 GPIO26 | A GPIO2, B GPIO15, gripper GPIO4 |
| J5 | Elevador TB6600 | GPIO22 | GPIO21 | PUL GPIO5, DIR GPIO18, ENA GPIO19 | Sin encoder documentado |

## Protocolo CAN documentado

| Tipo | ID base | Funcion |
|---|---|---|
| A | `0xA00n` | Solicitud de estado. |
| B | `0xB00n` | Respuesta de estado. |
| C | `0xC00n` | Comando de actuador. |
| D | `0xD00n` | Comandos generales, modo de control y gripper. |

## ROS 2 validado localmente

Se verifico la compilacion local del paquete principal:

```bash
cd ~/robot-project/ros2_ws
rm -rf build install log
colcon build --packages-select can_comm_pkg
source install/setup.bash
```

Tambien se verifico que `can_node` inicia correctamente cuando existe una interfaz `can0` virtual:

```bash
sudo modprobe vcan
sudo ip link add dev can0 type vcan 2>/dev/null || true
sudo ip link set up can0
ros2 run can_comm_pkg can_node
```

Salida esperada observada:

```text
CANNode iniciado y suscrito a /can_command
```

## BOM inicial

La BOM inicial esta en:

```text
docs/bom_template.csv
```

Resumen actual:

- 42 lineas de materiales/componentes.
- Costo registrado en Drive: S/ 1,048.18.
- Costo referencial agregado para componentes institucionales o sin costo: S/ 1,926.00.
- Costo estimado actual: S/ 2,749.18.

El costo estimado es preliminar. Debe revisarse antes de publicacion porque algunos componentes de UTEC figuran como S/ 0.00 y otros usan precios referenciales.

## Pendientes inmediatos

1. Probar entry points principales adicionales:

```bash
ros2 run can_comm_pkg control_teclado
ros2 run can_comm_pkg can_traj
```

2. Confirmar que no se suban artefactos generados:

```bash
git ls-files | grep -E '(^|/)(build|install|log|\.idea|\.vscode)(/|$)'
```

3. Completar diagramas electricos finales en `electronics/`.
4. Completar CAD/STEP/STL en `hardware/` cuando esten disponibles.
5. Curar resultados hacia `validation/`.
6. Crear `LICENSE` y `CITATION.cff`.

## Criterio de cierre para HardwareX

La rama estara lista para empezar el manuscrito cuando se cumpla:

- Firmware J1-J5 compila desde GitHub.
- ROS 2 compila desde GitHub.
- CAN fisico o virtual permite iniciar `can_node`.
- Existen diagramas electricos y pinouts finales.
- Existen archivos mecanicos o, si no se cuenta con CAD, se declara como pendiente critico.
- La BOM permite comprar o sustituir componentes.
- La validacion tiene datos y figuras curadas.

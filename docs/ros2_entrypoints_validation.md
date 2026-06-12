# Validación de entry points ROS 2

Este documento lista los comandos principales del paquete `can_comm_pkg` y define una rutina de validación reproducible.

## Fuente

Los entry points se definen en:

```text
ros2_ws/src/can_comm_pkg/setup.py
```

El archivo `setup.py` es la referencia principal para los comandos instalables del paquete.

## Preparación del entorno

```bash
cd ~/robot-project/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select can_comm_pkg
source install/setup.bash
```

## CAN virtual para pruebas sin hardware

```bash
sudo modprobe vcan
sudo ip link add dev can0 type vcan 2>/dev/null || true
sudo ip link set up can0
ip link show can0
```

## Comandos principales

| Comando | Función | Estado |
|---|---|---|
| `can_node` | Nodo base SocketCAN, publica/recibe mensajes CAN. | Validado con `vcan`. |
| `can_cli` | Interfaz CLI para comandos CAN. | Pendiente de prueba local. |
| `can_slider` | Interfaz con sliders para control articular. | Pendiente de prueba local. |
| `can_traj` | Ejecución de trayectorias. | Pendiente de prueba local. |
| `can_traj_trapezoid` | Ejecución de trayectoria trapezoidal. | Pendiente de prueba local. |
| `ik_node` | Nodo de cinemática inversa. | Pendiente de prueba local. |
| `control_teclado` | Control por teclado. | Evidencia de video identificada. |
| `control_teclado_trapezoidal` | Control por teclado con perfil trapezoidal. | Pendiente de prueba local. |
| `barcode_detector` | Detección de códigos de barras. | Pendiente de prueba local. |
| `product_identifier` | Identificación de producto. | Pendiente de prueba local. |

## Rutina mínima de prueba

En una terminal:

```bash
cd ~/robot-project/ros2_ws
source install/setup.bash
ros2 run can_comm_pkg can_node
```

En otra terminal:

```bash
cd ~/robot-project/ros2_ws
source install/setup.bash
ros2 run can_comm_pkg control_teclado
```

## Pruebas de trayectoria J5

```bash
ros2 run can_comm_pkg j5_ramp
ros2 run can_comm_pkg j5_trap
```

Estas pruebas deben relacionarse con:

```text
validation/media/j5_ramp_100mm_5reps.mp4
validation/media/j5_trapezoidal_100mm_5reps.mp4
validation/joint_motion_tests/j5_motion_summary.csv
```

## Cierre de CAN virtual

```bash
sudo ip link delete can0
```

## Resultado esperado

El objetivo mínimo sin hardware físico es confirmar que:

- el paquete compila;
- `can_node` inicia con `can0` virtual;
- los entry points existen;
- los comandos no fallan por importaciones faltantes;
- los módulos principales quedan listos para prueba física posterior.

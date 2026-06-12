# Manual de operación

Este manual describe la secuencia básica para compilar, ejecutar y probar el sistema desde ROS 2.

## Requisitos

- Ubuntu con ROS 2 Jazzy instalado.
- Workspace del proyecto en `~/robot-project/ros2_ws`.
- Interfaz CAN física `can0` o interfaz virtual `vcan` para pruebas sin hardware.
- ESP-IDF instalado fuera del repositorio para programar los ESP32.

## Compilación de ROS 2

```bash
cd ~/robot-project/ros2_ws
source /opt/ros/jazzy/setup.bash
rm -rf build install log
colcon build --packages-select can_comm_pkg
source install/setup.bash
```

## Prueba sin hardware usando CAN virtual

```bash
sudo modprobe vcan
sudo ip link add dev can0 type vcan 2>/dev/null || true
sudo ip link set up can0
ip link show can0
```

Iniciar el nodo CAN:

```bash
ros2 run can_comm_pkg can_node
```

Salida esperada:

```text
CANNode iniciado y suscrito a /can_command
```

## Prueba con CAN físico

Cuando esté conectada la interfaz CAN física:

```bash
sudo ip link set can0 down 2>/dev/null || true
sudo ip link set can0 up type can bitrate 500000
ip -details link show can0
candump can0
```

En otra terminal:

```bash
cd ~/robot-project/ros2_ws
source install/setup.bash
ros2 run can_comm_pkg can_node
```

## Comandos principales

| Comando | Uso |
|---|---|
| `ros2 run can_comm_pkg can_node` | Inicia el puente ROS 2 / SocketCAN. |
| `ros2 run can_comm_pkg control_teclado` | Control por teclado. |
| `ros2 run can_comm_pkg can_traj` | Ejecuta trayectoria desde ROS 2. |
| `ros2 run can_comm_pkg can_slider` | Control por sliders. |
| `ros2 run can_comm_pkg ik_node` | Nodo de cinemática inversa. |
| `ros2 run can_comm_pkg j5_ramp` | Prueba del elevador J5 con perfil rampa. |
| `ros2 run can_comm_pkg j5_trap` | Prueba del elevador J5 con perfil trapezoidal. |

## Programación de firmware ESP32

Cargar ESP-IDF:

```bash
source /media/F15/Data/ESP_IDF_CONTAINER/v5.3.3/esp-idf/export.sh
```

Compilar un nodo, por ejemplo J1:

```bash
cd ~/robot-project/firmware/esp32_joint_node/J1
idf.py set-target esp32
idf.py build
```

Flashear cuando el ESP32 esté conectado:

```bash
idf.py -p /dev/ttyUSB0 flash monitor
```

## Secuencia de encendido recomendada

1. Verificar cableado de potencia y tierra común.
2. Verificar terminaciones CAN de 120 ohmios en los extremos del bus.
3. Encender alimentación lógica.
4. Encender alimentación de actuadores.
5. Levantar `can0`.
6. Ejecutar `can_node`.
7. Ejecutar el comando de control o prueba.

## Secuencia de apagado recomendada

1. Detener comandos ROS 2 activos.
2. Detener `can_node`.
3. Apagar alimentación de actuadores.
4. Apagar alimentación lógica.
5. Desconectar alimentación principal si se trabaja sobre el cableado.

## Parada o incidencia

Si el movimiento no es esperado:

- detener el proceso ROS 2 con `Ctrl+C`;
- cortar alimentación de actuadores;
- revisar CANH/CANL;
- revisar tierra común;
- revisar IDs CAN;
- revisar alimentación del nodo ESP32 correspondiente.

## Documentos relacionados

- `docs/ros2_entrypoints_validation.md`
- `docs/troubleshooting.md`
- `firmware/ESP_IDF_BUILD_GUIDE.md`
- `electronics/pinout_tables/esp32_pinout_table.md`

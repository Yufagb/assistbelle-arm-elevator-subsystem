# Troubleshooting

Esta guia registra errores reales encontrados durante la preparacion de la rama HardwareX.

## 1. Error al abrir una terminal nueva: `setup.bash: No such file or directory`

### Sintoma

Al abrir una nueva terminal aparece algo como:

```text
bash: /home/f15/rosario_ws/install/setup.bash: No such file or directory
```

### Causa

El archivo `.bashrc` esta intentando cargar automaticamente un workspace ROS que ya no existe o que todavia no fue compilado.

### Solucion rapida

Abrir `.bashrc`:

```bash
nano ~/.bashrc
```

Buscar lineas parecidas a:

```bash
source /home/f15/rosario_ws/install/setup.bash
source /home/f15/robot-project/ros2_ws/install/setup.bash
```

Comentar la linea antigua o inexistente:

```bash
# source /home/f15/rosario_ws/install/setup.bash
```

Para el workspace actual, usar carga condicional:

```bash
if [ -f "$HOME/robot-project/ros2_ws/install/setup.bash" ]; then
  source "$HOME/robot-project/ros2_ws/install/setup.bash"
fi
```

Guardar y recargar:

```bash
source ~/.bashrc
```

## 2. Error ROS 2: `OSError: [Errno 19] No such device`

### Sintoma

Al ejecutar:

```bash
ros2 run can_comm_pkg can_node
```

aparece:

```text
OSError: [Errno 19] No such device
```

### Causa

El nodo intenta abrir la interfaz CAN `can0`, pero el sistema operativo no tiene una interfaz `can0` activa. Esto es normal si no esta conectada la interfaz CAN fisica o si todavia no se configuro SocketCAN.

### Verificacion

```bash
ip link show
```

Si no aparece `can0`, el nodo no puede iniciar contra hardware real.

### Opcion A: usar CAN fisico

Con MCP2515 o interfaz CAN conectada:

```bash
sudo ip link set can0 down 2>/dev/null || true
sudo ip link set can0 up type can bitrate 500000
ip -details link show can0
candump can0
```

### Opcion B: probar sin hardware usando CAN virtual

```bash
sudo modprobe vcan
sudo ip link add dev can0 type vcan
sudo ip link set up can0
ip link show can0
```

Luego:

```bash
ros2 run can_comm_pkg can_node
```

Para eliminar la interfaz virtual:

```bash
sudo ip link delete can0
```

## 3. Advertencias ROS 2 sobre `ROS_LOCALHOST_ONLY`

### Sintoma

Aparecen advertencias como:

```text
ROS_LOCALHOST_ONLY is deprecated
```

### Causa

Es una advertencia de configuracion de ROS 2. No impide compilar ni ejecutar el paquete.

### Solucion opcional

Revisar `.bashrc` y quitar configuraciones antiguas de `ROS_LOCALHOST_ONLY` si no se usan.

## 4. Error ESP-IDF: `idf.py: command not found`

### Causa

ESP-IDF no esta cargado en la terminal.

### Solucion

Cargar ESP-IDF desde la instalacion externa:

```bash
source /media/F15/Data/ESP_IDF_CONTAINER/v5.3.3/esp-idf/export.sh
idf.py --version
```

## 5. Error ESP-IDF: `No module named click`

### Causa

El entorno Python de ESP-IDF esta incompleto.

### Solucion

```bash
export IDF_PATH=/media/F15/Data/ESP_IDF_CONTAINER/v5.3.3/esp-idf
/usr/bin/python3 "$IDF_PATH/tools/idf_tools.py" install-python-env
source "$IDF_PATH/export.sh"
idf.py --version
```

## 6. Checks generales

- Verificar que la interfaz CAN este activa.
- Verificar que cada nodo ESP32 tenga energia.
- Verificar que CANH y CANL no esten invertidos.
- Verificar resistencias de terminacion de 120 ohmios en los extremos del bus.
- Verificar que el entorno ROS 2 este cargado.
- Verificar dependencias Python.
- Verificar indice de camara antes de correr scripts de vision.

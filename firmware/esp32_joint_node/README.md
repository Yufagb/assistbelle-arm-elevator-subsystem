# Nodos ESP32 J1-J4

Esta carpeta contiene los proyectos ESP-IDF de las articulaciones rotativas del brazo.

## Nodos

| Nodo | Articulacion | Funcion | Estado |
|---|---|---|---|
| J1 | Base | Control de motor DC con encoder | Compila localmente |
| J2 | Hombro | Control de motor DC con encoder | Compila localmente |
| J3 | Codo | Control de motor DC con encoder | Compila localmente |
| J4 | Muneca y gripper | Control de motor DC con encoder y servo de gripper | Compila localmente |

## Estructura de cada proyecto

Cada nodo contiene un proyecto ESP-IDF independiente:

```text
Jx/
├── CMakeLists.txt
├── sdkconfig
└── main/
    ├── CMakeLists.txt
    ├── main.c
    ├── base_libs.h
    ├── encoder_driver.h
    ├── motor_driver.h
    ├── node_config.h
    ├── pid_controller.h
    └── twai_comms.h
```

J4 tambien incluye `grip_controller.h` para el control del gripper.

## Compilacion rapida

```bash
source /media/F15/Data/ESP_IDF_CONTAINER/v5.3.3/esp-idf/export.sh
cd ~/robot-project/firmware/esp32_joint_node/J1
idf.py set-target esp32
idf.py build
```

Cambiar `J1` por `J2`, `J3` o `J4`.

## Documentacion relacionada

- Pines por nodo: `../../electronics/pinout_tables/esp32_pinout_table.md`.
- Protocolo CAN: `../can_protocol/can_messages.md`.
- Guia ESP-IDF: `../ESP_IDF_BUILD_GUIDE.md`.

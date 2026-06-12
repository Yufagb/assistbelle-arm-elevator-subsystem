# Nodo ESP32 J5 - Elevador

Esta carpeta contiene el firmware ESP-IDF del eje prismatico J5, asociado al sistema de elevacion con motores NEMA y driver TB6600.

## Proyecto disponible

| Proyecto | Funcion | Estado |
|---|---|---|
| J5_tb6600 | Control del elevador mediante STEP, DIR y ENA | Compila localmente |

## Estructura

```text
J5_tb6600/
├── CMakeLists.txt
├── sdkconfig
└── main/
    ├── CMakeLists.txt
    ├── Kconfig.projbuild
    └── twai_network_example_slave_main.c
```

## Pines principales

| Funcion | GPIO ESP32 |
|---|---:|
| CAN TX | GPIO22 |
| CAN RX | GPIO21 |
| TB6600 ENA | GPIO19 |
| TB6600 DIR | GPIO18 |
| TB6600 PUL | GPIO5 |

## Compilacion rapida

```bash
source /media/F15/Data/ESP_IDF_CONTAINER/v5.3.3/esp-idf/export.sh
cd ~/robot-project/firmware/esp32_stepper_node/J5_tb6600
idf.py set-target esp32
idf.py build
```

## Documentacion relacionada

- Pines por nodo: `../../electronics/pinout_tables/esp32_pinout_table.md`.
- Protocolo CAN: `../can_protocol/can_messages.md`.
- Guia ESP-IDF: `../ESP_IDF_BUILD_GUIDE.md`.

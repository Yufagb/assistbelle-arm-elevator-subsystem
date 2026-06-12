# Firmware ESP32

Esta carpeta contiene los proyectos ESP-IDF usados para programar los microcontroladores ESP32 del robot.

## Estructura

- ESP_IDF_BUILD_GUIDE.md: guia para compilar y programar.
- import_firmware_from_zips.sh: script auxiliar para importar los ZIP originales.
- can_protocol: documentacion de mensajes CAN.
- esp32_joint_node: nodos J1, J2, J3 y J4.
- esp32_stepper_node: nodo J5 del elevador con TB6600.

## Nodos disponibles

| Nodo | Subsistema | Carpeta | Estado |
|---|---|---|---|
| J1 | Base | esp32_joint_node/J1 | Compila localmente |
| J2 | Hombro | esp32_joint_node/J2 | Compila localmente |
| J3 | Codo | esp32_joint_node/J3 | Compila localmente |
| J4 | Muneca y gripper | esp32_joint_node/J4 | Compila localmente |
| J5 | Elevador TB6600 | esp32_stepper_node/J5_tb6600 | Compila localmente |

## Guia principal

Usar ESP_IDF_BUILD_GUIDE.md para cargar ESP-IDF, compilar, flashear y abrir los proyectos con VS Code.

## Dependencia externa

ESP-IDF no se versiona dentro del repositorio porque es una dependencia pesada. Debe estar instalado fuera del repositorio, por ejemplo en el disco externo donde se tenga ESP_IDF_CONTAINER.

## Relacion con electronica

- Pines por nodo: electronics/pinout_tables/esp32_pinout_table.md.
- Protocolo CAN: firmware/can_protocol/can_messages.md.
- Bus principal: electronics/wiring_diagrams/bus_principal.md.
- Nodos controladores: electronics/wiring_diagrams/nodos_controladores.md.

## Archivos que no deben subirse

No versionar salidas de compilacion ni configuraciones locales: build, .vscode, .devcontainer, .clangd, binarios, mapas, ELF ni sdkconfig.old.

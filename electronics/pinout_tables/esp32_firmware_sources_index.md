# Indice de fuentes para completar pinout ESP32

Este archivo relaciona las carpetas de Drive con las carpetas del repositorio para completar las tablas de pines.

## Fuentes revisadas

| Drive | Contenido | Destino en GitHub |
|---|---|---|
| JointVelocityControllers/J1 | Proyecto ESP-IDF de articulacion J1 | firmware/esp32_joint_node/J1 |
| JointVelocityControllers/J2 | Proyecto ESP-IDF de articulacion J2 | firmware/esp32_joint_node/J2 |
| JointVelocityControllers/J3 | Proyecto ESP-IDF de articulacion J3 | firmware/esp32_joint_node/J3 |
| JointVelocityControllers/J4 | Proyecto ESP-IDF de articulacion J4 y gripper | firmware/esp32_joint_node/J4 |
| JointPositionControllers/twai_id_based_basedness | Prueba o base de comunicacion TWAI/CAN | firmware/esp32_stepper_node/J5 o firmware/can_protocol |
| JointPositionControllers/codigo para diferentes nodos | Archivos nodo1.c a nodo4.c | revisar antes de migrar |

## Archivos clave a revisar

Para cada J1-J4:

- `main/node_config.h`: IDs de nodo, configuracion de articulacion y posiblemente pines.
- `main/motor_driver.h`: pines de driver DC.
- `main/encoder_driver.h`: pines del encoder.
- `main/twai_comms.h`: pines TWAI/CAN y bitrate.
- `main/grip_controller.h`: pines del gripper en J4, si aplica.

Para J5/elevador:

- archivo principal `.c` del proyecto final usado.
- definiciones STEP/DIR/EN.
- definiciones de TWAI/CAN.

## Tabla pendiente de completar

| Nodo | Archivo fuente esperado | Pines que faltan |
|---|---|---|
| J1 | node_config.h, motor_driver.h, encoder_driver.h, twai_comms.h | CAN TX/RX, PWM/DIR, encoder A/B. |
| J2 | node_config.h, motor_driver.h, encoder_driver.h, twai_comms.h | CAN TX/RX, RPWM/LPWM/R_EN/L_EN, encoder A/B. |
| J3 | node_config.h, motor_driver.h, encoder_driver.h, twai_comms.h | CAN TX/RX, RPWM/LPWM/R_EN/L_EN, encoder A/B. |
| J4 | node_config.h, motor_driver.h, encoder_driver.h, grip_controller.h, twai_comms.h | CAN TX/RX, motor DC, encoder A/B, servo PWM. |
| J5 | archivo final del elevador | CAN TX/RX, STEP, DIR, EN para motores PaP. |

## Nota

El conector permitio listar y ubicar los archivos de Drive, pero no devolvio el contenido textual de los `.c` y `.h`. Por eso queda preparada la estructura y la relacion de archivos, pero la extraccion exacta de pines debe hacerse copiando los archivos fuente a GitHub o compartiendolos como ZIP/archivo adjunto en el chat.

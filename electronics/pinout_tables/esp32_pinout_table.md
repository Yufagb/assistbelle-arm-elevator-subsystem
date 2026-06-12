# Tabla de pines ESP32

Documento generado a partir de los ZIP subidos al chat:

- `JointPosition y JointVelocity Controllers.zip`
- `can-controll-.zip`

Los pines fueron extraidos principalmente de `node_config.h` para J1-J4 y de `twai_network_example_slave_main.c` para J5/elevador.

## Resumen por nodo

| Nodo | Subsistema | Driver | CAN TX | CAN RX | Motor IN1 / STEP | Motor IN2 / DIR | ENA | Encoder A | Encoder B | Gripper |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| J1 | Base | DRV8871 | GPIO21 | GPIO22 | GPIO32 | GPIO33 | - | GPIO10 | GPIO13 | No |
| J2 | Hombro | DRV8871 / etapa DC | GPIO22 | GPIO21 | GPIO5 | GPIO17 | - | GPIO19 | GPIO18 | No |
| J3 | Codo | DRV8871 / etapa DC | GPIO21 | GPIO22 | GPIO32 | GPIO33 | - | GPIO10 | GPIO13 | No |
| J4 | Muneca + gripper | DRV8871 / etapa DC + servo | GPIO33 | GPIO32 | GPIO25 | GPIO26 | - | GPIO2 | GPIO15 | GPIO4 |
| J5 | Elevador prismático | TB6600 | GPIO22 | GPIO21 | PUL GPIO5 | DIR GPIO18 | GPIO19 | - | - | No |

## J1 - Base

Fuente: `JointVelocityControllers/J1/main/node_config.h`.

| Funcion | GPIO ESP32 | Definicion en firmware |
|---|---:|---|
| CAN TX | GPIO21 | `TX_GPIO_NUM` |
| CAN RX | GPIO22 | `RX_GPIO_NUM` |
| Driver IN1 | GPIO32 | `DRV_IN1` |
| Driver IN2 | GPIO33 | `DRV_IN2` |
| Encoder A | GPIO10 | `ENCODER_A_PIN` |
| Encoder B | GPIO13 | `ENCODER_B_PIN` |
| ILIM | Interno por DAC | `ILIM_CONNECTED`, `DAC_CHAN_0` |

IDs CAN:

| Mensaje | ID |
|---|---:|
| Solicitud de estado | `0x0A1` |
| Respuesta de estado | `0x0B1` |
| Cambio de setpoint | `0x0C1` |
| Modo de control | `0x0D1` |
| Broadcast estado | `0x0A6` |

## J2 - Hombro

Fuente: `JointVelocityControllers/J2/main/node_config.h`.

| Funcion | GPIO ESP32 | Definicion en firmware |
|---|---:|---|
| CAN TX | GPIO22 | `TX_GPIO_NUM` |
| CAN RX | GPIO21 | `RX_GPIO_NUM` |
| Driver IN1 | GPIO5 | `DRV_IN1` |
| Driver IN2 | GPIO17 | `DRV_IN2` |
| Encoder A | GPIO19 | `ENCODER_A_PIN` |
| Encoder B | GPIO18 | `ENCODER_B_PIN` |
| ILIM | Interno por DAC | `ILIM_CONNECTED`, `DAC_CHAN_0` |

IDs CAN:

| Mensaje | ID |
|---|---:|
| Solicitud de estado | `0x0A2` |
| Respuesta de estado | `0x0B2` |
| Cambio de setpoint | `0x0C2` |
| Modo de control | `0x0D1` |
| Broadcast estado | `0x0A6` |

## J3 - Codo

Fuente: `JointVelocityControllers/J3/main/node_config.h`.

| Funcion | GPIO ESP32 | Definicion en firmware |
|---|---:|---|
| CAN TX | GPIO21 | `TX_GPIO_NUM` |
| CAN RX | GPIO22 | `RX_GPIO_NUM` |
| Driver IN1 | GPIO32 | `DRV_IN1` |
| Driver IN2 | GPIO33 | `DRV_IN2` |
| Encoder A | GPIO10 | `ENCODER_A_PIN` |
| Encoder B | GPIO13 | `ENCODER_B_PIN` |
| ILIM | Interno por DAC | `ILIM_CONNECTED`, `DAC_CHAN_0` |

IDs CAN:

| Mensaje | ID |
|---|---:|
| Solicitud de estado | `0x0A3` |
| Respuesta de estado | `0x0B3` |
| Cambio de setpoint | `0x0C3` |
| Modo de control | `0x0D1` |
| Broadcast estado | `0x0A6` |

## J4 - Muneca y gripper

Fuente: `JointVelocityControllers/J4/main/node_config.h`.

| Funcion | GPIO ESP32 | Definicion en firmware |
|---|---:|---|
| CAN TX | GPIO33 | `TX_GPIO_NUM` |
| CAN RX | GPIO32 | `RX_GPIO_NUM` |
| Driver IN1 | GPIO25 | `DRV_IN1` |
| Driver IN2 | GPIO26 | `DRV_IN2` |
| Encoder A | GPIO2 | `ENCODER_A_PIN` |
| Encoder B | GPIO15 | `ENCODER_B_PIN` |
| Servo gripper | GPIO4 | `GRIPPER_PIN` |

IDs CAN:

| Mensaje | ID |
|---|---:|
| Solicitud de estado | `0x0A4` |
| Respuesta de estado | `0x0B4` |
| Cambio de setpoint | `0x0C4` |
| Modo de control | `0x0D1` |
| Comando gripper | `0x0D2` |
| Broadcast estado | `0x0A6` |

## J5 - Elevador / motores NEMA 23

Fuente: `can-controll-/main/twai_network_example_slave_main.c`.

| Funcion | GPIO ESP32 | Definicion en firmware |
|---|---:|---|
| CAN TX | GPIO22 | `CAN_TX_GPIO` |
| CAN RX | GPIO21 | `CAN_RX_GPIO` |
| TB6600 ENA | GPIO19 | `ENA_PIN` |
| TB6600 DIR | GPIO18 | `DIR_PIN` |
| TB6600 PUL | GPIO5 | `PUL_PIN` |

IDs CAN:

| Mensaje | ID |
|---|---:|
| Solicitud de posicion J5 | `0x0A5` / `0xA5` |
| Broadcast solicitud | `0x0A6` / `0xA6` |
| Respuesta posicion J5 | `0x0B5` / `0xB5` |
| Comando posicion J5 | `0x0C5` / `0xC5` |

## Parametros relevantes

| Nodo | PPR encoder | Reduccion | Filtro velocidad | Frecuencia control |
|---|---:|---:|---:|---:|
| J1 | 68 | 131 | 0.01 | 500 Hz |
| J2 | 68 | 19*50 | 0.01 | 500 Hz |
| J3 | 64 | 1000*1.0125 | 0.01 | 500 Hz |
| J4 | 64 | 131 | 0.25 | 500 Hz |
| J5 | - | tornillo T8, lead 8 mm | - | 500 pulsos/s |

## Observaciones

- J1, J2 y J3 tienen `ILIM_CONNECTED`; J4 no.
- J4 define `NODE_HAS_GRIPPER` y usa `GRIPPER_PIN GPIO4`.
- J5 usa TB6600 con `ENA=GPIO19`, `DIR=GPIO18`, `PUL=GPIO5`.
- La comunicacion CAN/TWAI trabaja a 500 kbit/s.
- Algunos comentarios internos de los archivos indican nombres de nodos distintos; para documentacion se toma como referencia el nombre de la carpeta J1-J4 y los IDs CAN definidos.

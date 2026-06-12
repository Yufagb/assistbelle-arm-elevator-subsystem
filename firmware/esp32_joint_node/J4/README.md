# Nodo ESP32 J4 - Muneca y gripper

Firmware de control para la articulacion J4 y el efector final del brazo robotico.

Fuente: ZIP `JointPosition y JointVelocity Controllers.zip`, carpeta `JointVelocityControllers/J4`.

## Pines principales

| Funcion | GPIO ESP32 |
|---|---:|
| CAN TX | GPIO33 |
| CAN RX | GPIO32 |
| Driver IN1 | GPIO25 |
| Driver IN2 | GPIO26 |
| Encoder A | GPIO2 |
| Encoder B | GPIO15 |
| Servo gripper | GPIO4 |

## IDs CAN

| Mensaje | ID |
|---|---:|
| Solicitud de estado | `0x0A4` |
| Respuesta de estado | `0x0B4` |
| Cambio de setpoint | `0x0C4` |
| Modo de control | `0x0D1` |
| Comando de gripper | `0x0D2` |
| Broadcast estado | `0x0A6` |

## Parametros

| Parametro | Valor |
|---|---:|
| Encoder PPR | 64 |
| Reduccion | 131 |
| Frecuencia de control | 500 Hz |
| Kp | 200 |
| Ki | 15 |
| Kd | 0 |
| Gripper | Activado en firmware |

## Archivos subidos

Por ahora se subio `main/node_config.h` como archivo clave de configuracion. Los demas archivos fuente del proyecto ESP-IDF deben copiarse despues si se desea compilar directamente desde esta carpeta.

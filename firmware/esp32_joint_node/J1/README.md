# Nodo ESP32 J1 - Base

Firmware de control de velocidad/posicion para la articulacion J1 del brazo robotico.

Fuente: ZIP `JointPosition y JointVelocity Controllers.zip`, carpeta `JointVelocityControllers/J1`.

## Pines principales

| Funcion | GPIO ESP32 |
|---|---:|
| CAN TX | GPIO21 |
| CAN RX | GPIO22 |
| Driver IN1 | GPIO32 |
| Driver IN2 | GPIO33 |
| Encoder A | GPIO10 |
| Encoder B | GPIO13 |

## IDs CAN

| Mensaje | ID |
|---|---:|
| Solicitud de estado | `0x0A1` |
| Respuesta de estado | `0x0B1` |
| Cambio de setpoint | `0x0C1` |
| Modo de control | `0x0D1` |
| Broadcast estado | `0x0A6` |

## Parametros

| Parametro | Valor |
|---|---:|
| Encoder PPR | 68 |
| Reduccion | 131 |
| Frecuencia de control | 500 Hz |
| Kp | 200 |
| Ki | 15 |
| Kd | 0 |

## Archivos subidos

Por ahora se subio `main/node_config.h` como archivo clave de configuracion. Los demas archivos fuente del proyecto ESP-IDF deben copiarse despues si se desea compilar directamente desde esta carpeta.

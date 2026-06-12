# Nodo ESP32 J3 - Codo

Firmware de control para la articulacion J3 del brazo robotico.

Fuente: ZIP `JointPosition y JointVelocity Controllers.zip`, carpeta `JointVelocityControllers/J3`.

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
| Solicitud de estado | `0x0A3` |
| Respuesta de estado | `0x0B3` |
| Cambio de setpoint | `0x0C3` |
| Modo de control | `0x0D1` |
| Broadcast estado | `0x0A6` |

## Parametros

| Parametro | Valor |
|---|---:|
| Encoder PPR | 64 |
| Reduccion | 1000*1.0125 |
| Encoder invertido | Si |
| Frecuencia de control | 500 Hz |
| Kp | 200 |
| Ki | 15.5 |
| Kd | 0 |

## Archivos subidos

Por ahora se subio `main/node_config.h` como archivo clave de configuracion. Los demas archivos fuente del proyecto ESP-IDF deben copiarse despues si se desea compilar directamente desde esta carpeta.

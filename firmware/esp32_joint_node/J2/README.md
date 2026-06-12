# Nodo ESP32 J2 - Hombro

Firmware de control para la articulacion J2 del brazo robotico.

Fuente: ZIP `JointPosition y JointVelocity Controllers.zip`, carpeta `JointVelocityControllers/J2`.

## Pines principales

| Funcion | GPIO ESP32 |
|---|---:|
| CAN TX | GPIO22 |
| CAN RX | GPIO21 |
| Driver IN1 | GPIO5 |
| Driver IN2 | GPIO17 |
| Encoder A | GPIO19 |
| Encoder B | GPIO18 |

## IDs CAN

| Mensaje | ID |
|---|---:|
| Solicitud de estado | `0x0A2` |
| Respuesta de estado | `0x0B2` |
| Cambio de setpoint | `0x0C2` |
| Modo de control | `0x0D1` |
| Broadcast estado | `0x0A6` |

## Parametros

| Parametro | Valor |
|---|---:|
| Encoder PPR | 68 |
| Reduccion | 19*50 |
| Encoder invertido | Si |
| Frecuencia de control | 500 Hz |
| Kp | 200 |
| Ki | 15 |
| Kd | 0 |

## Archivos subidos

Por ahora se subio `main/node_config.h` como archivo clave de configuracion. Los demas archivos fuente del proyecto ESP-IDF deben copiarse despues si se desea compilar directamente desde esta carpeta.

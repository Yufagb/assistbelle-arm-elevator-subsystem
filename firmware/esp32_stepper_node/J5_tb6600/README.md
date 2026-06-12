# Nodo ESP32 J5 - Elevador con TB6600

Firmware recuperado desde el ZIP `can-controll-.zip`.

## Funcion

Controla el eje prismatico J5 del sistema de elevacion mediante driver TB6600 y comunicacion CAN/TWAI a 500 kbit/s.

## Pines principales

| Funcion | GPIO ESP32 | Definicion |
|---|---:|---|
| CAN TX | GPIO22 | `CAN_TX_GPIO` |
| CAN RX | GPIO21 | `CAN_RX_GPIO` |
| TB6600 ENA | GPIO19 | `ENA_PIN` |
| TB6600 DIR | GPIO18 | `DIR_PIN` |
| TB6600 PUL | GPIO5 | `PUL_PIN` |

## IDs CAN

| Mensaje | ID |
|---|---:|
| Solicitud de posicion | `0x0A5` / `0xA5` |
| Broadcast solicitud | `0x0A6` / `0xA6` |
| Respuesta de posicion | `0x0B5` / `0xB5` |
| Comando de posicion | `0x0C5` / `0xC5` |

## Parametros mecanicos

| Parametro | Valor |
|---|---:|
| Pasos completos por vuelta | 200 |
| Avance del tornillo T8 | 8 mm |
| Velocidad de pulsos | 500 pulsos/s |

## Pendientes

- Agregar `CMakeLists.txt` si se confirma como firmware final.
- Confirmar si el hardware final usa un TB6600 por motor o un esquema compartido.
- Confirmar formato final del comando de posicion desde ROS 2.

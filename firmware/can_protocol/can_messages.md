# Mensajes CAN del sistema

Este documento resume el protocolo CAN actualmente documentado para el subsistema brazo/elevador de Assistbelle y cruza la tesis, firmware ESP32 y ROS 2.

## Convención de IDs

La tesis describe conceptualmente el formato:

```text
ID = 0xn00m
```

En la implementación actual de ROS 2 y firmware ESP32, los IDs usados en SocketCAN/TWAI son IDs estándar de 11 bits en formato corto:

```text
A1..A6, B1..B5, C1..C6, D1..D2
```

En código, `can_node.py` calcula el ID como:

```text
A: 0xA0 | motor
B: 0xB0 | motor
C: 0xC0 | motor
D: 0xD0 | motor
```

Por ejemplo, `C5` se transmite como `0xC5` y `A6` como `0xA6`.

## Tipos de mensajes

| Tipo | Dirección | ID actual | Función |
|---|---|---|---|
| A | Maestro a nodo | `0xA1` a `0xA5`, broadcast `0xA6` | Solicitud de estado. |
| B | Nodo a maestro | `0xB1` a `0xB5` | Respuesta de estado. |
| C | Maestro a nodo | `0xC1` a `0xC5`, auxiliar `0xC6` | Comando de actuador. |
| D | Maestro a nodo | `0xD1`, `0xD2` | Comandos generales / gripper. |

## Payload estándar recomendado

Para mantener compatibilidad entre ROS 2 y firmware final, se recomienda congelar estos payloads:

| Mensaje | ID | DLC | Payload | Unidad | Endianness | Estado |
|---|---:|---:|---|---|---|---|
| Solicitud estado J1 | `0xA1` | 0 | Sin payload | - | - | Implementado en ROS 2. |
| Solicitud estado J2 | `0xA2` | 0 | Sin payload | - | - | Implementado en ROS 2. |
| Solicitud estado J3 | `0xA3` | 0 | Sin payload | - | - | Implementado en ROS 2. |
| Solicitud estado J4 | `0xA4` | 0 | Sin payload | - | - | Implementado en ROS 2. |
| Solicitud estado J5 | `0xA5` | 0 | Sin payload | - | - | Implementado en ROS 2 y firmware J5. |
| Broadcast solicitud | `0xA6` | 0 | Sin payload | - | - | Implementado en ROS 2 y firmware J5. |
| Estado J1-J4 | `0xB1`-`0xB4` | 8 | `float32 position`, `float32 velocity` | rad, rad/s | little-endian | Estándar ROS 2 esperado. |
| Estado J5 recomendado | `0xB5` | 8 | `float32 position`, `float32 velocity` | mm, mm/s | little-endian | Recomendado para compatibilidad final ROS 2. |
| Comando J1-J4 | `0xC1`-`0xC4` | 8 | `float32 target_position`, `float32 target_velocity` | rad, rad/s | little-endian | Implementado en ROS 2. |
| Comando J5 | `0xC5` | 4 | `float32 target_position` | mm | little-endian | Implementado en ROS 2 y aceptado por firmware J5. |
| Auxiliar / reset J5 | `0xC6` | 1 | `uint8 command` | adimensional | byte | Implementado en ROS 2 como auxiliar; semántica final pendiente. |
| Modo de control | `0xD1` | 4 | `float32 mode/value` | adimensional | little-endian | Requiere cierre semántico final. |
| Gripper | `0xD2` | 4 | `float32 opening_percent` | % | little-endian | Documentado para efector final. |

## Estado actual de compatibilidad J5

### ROS 2 actual

`can_node.py` envía `C5` como un solo `float32` little-endian en milímetros:

```text
C5:<target_mm>  ->  payload = struct.pack('<f', target_mm)
```

También interpreta todo mensaje `B1..B5` con DLC >= 8 como:

```text
position, velocity = struct.unpack('<ff', payload[:8])
```

Por eso, para J5, ROS 2 espera:

```text
B5 = float32 position_mm + float32 velocity_mm_s
```

### Firmware J5 actual

El firmware J5 actual acepta `C5` en dos formatos:

| Formato recibido | Interpretación |
|---|---|
| DLC = 4 | `float32` little-endian, redondeado a mm. |
| DLC >= 2 | `int16` big-endian, mm. |

Para `A5` o `A6`, el firmware responde `B5` con DLC = 8:

```text
bytes 0..3 = float32 position_mm little-endian
bytes 4..7 = 04 00 00 80
```

Esto reporta correctamente la posición, pero **no es totalmente compatible con la expectativa actual de ROS 2**, porque ROS 2 interpreta los bytes 4..7 como `float32 velocity`.

## Recomendación de cierre

Para cerrar el protocolo antes de HardwareX, se recomienda una de estas dos opciones:

### Opción A — recomendada

Actualizar firmware J5 para que `B5` responda:

```text
bytes 0..3 = float32 position_mm little-endian
bytes 4..7 = float32 velocity_mm_s little-endian
```

Si no se mide velocidad de J5, enviar `0.0f` como velocidad.

Ventaja: no requiere casos especiales en ROS 2 y mantiene el mismo formato `B1..B5`.

### Opción B

Mantener firmware J5 como está y modificar `can_node.py` para tratar `B5` como caso especial:

```text
B5 bytes 0..3 = position_mm
B5 bytes 4..7 = status/reserved
```

Ventaja: conserva firmware actual. Desventaja: rompe la uniformidad del protocolo y requiere documentar bytes reservados.

## Parámetros J5 relevantes

| Parámetro | Valor actual en firmware J5 | Observación |
|---|---:|---|
| Motor | NEMA 23 | Dos motores controlados por dos TB6600. |
| Driver | TB6600 x2 | `PUL`, `DIR`, `ENA` compartidos en paralelo por diseño. |
| Lead screw | T8, lead 8 mm | Usado para convertir pasos a mm. |
| Full steps/rev | 200 | Firmware. |
| Microstep actual | 1 | Según DIP S1=1, S2=1, S3=0 en firmware. |
| Pulses/mm actual | 25 | `(200 * microstep) / 8`. |
| Pulse rate | 500 pulses/s | `SPEED_HZ`. |
| CAN bitrate | 500 kbit/s | TWAI / SocketCAN. |

## Pendientes

- Confirmar físicamente el voltaje de alimentación de ambos TB6600.
- Decidir si se aplicará la opción A o B para `B5`.
- Confirmar semántica final de `C6`.
- Confirmar si `D2` responde solo en J4/gripper o en otro nodo final.
- Documentar límites de seguridad J5: mínimo, máximo, homing y fin de carrera si aplica.

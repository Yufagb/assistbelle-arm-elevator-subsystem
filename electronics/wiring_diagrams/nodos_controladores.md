# Nodos controladores

Documento generado a partir de la tesis y de los diagramas del Anexo 11.

## Arquitectura general

La tesis describe 5 nodos controladores basados en ESP32 y comunicacion CAN mediante transceptores SN65HVD230D.

| Nodo | Actuador / subsistema | Driver | Funcion principal |
|---|---|---|---|
| Nodo 1 | Articulacion 1 / base | DRV8871 | Motor DC con encoder de cuadratura. |
| Nodo 2 | Articulacion 2 / hombro | IBT-2 | Motor DC con encoder de cuadratura. |
| Nodo 3 | Articulacion 3 / codo | IBT-2 | Motor DC con encoder de cuadratura. |
| Nodo 4 | Articulacion 4 / muneca + gripper | DRV8871 + servo | Motor DC con encoder y control de pinza. |
| Nodo 5 | Elevador / eje prismatico | TB6600 | Dos motores paso a paso NEMA 23. |

## Nodo DC con DRV8871

El diagrama del Anexo 11.2 muestra un nodo basado en ESP32 DevKit y SN65HVD230D para bus CAN.

Senales principales:

| Senal | Funcion |
|---|---|
| PWM / control motor | Entrada de control hacia el DRV8871. |
| Encoder A | Fase A del codificador. |
| Encoder B | Fase B del codificador. |
| CAN TX/RX | Comunicacion logica ESP32 hacia transceptor CAN. |
| CANH/CANL | Lineas diferenciales hacia bus CAN. |
| 12V | Potencia de motor. |
| 5V / 3.3V | Logica segun modulo usado. |
| GND | Tierra comun. |

## Nodo DC con IBT-2

El diagrama del Anexo 11.3 muestra el uso de IBT-2 para motores DC de mayor corriente.

Senales principales:

| Senal | Funcion |
|---|---|
| RPWM | PWM en direccion positiva. |
| LPWM | PWM en direccion negativa. |
| R_EN | Habilitacion lado derecho. |
| L_EN | Habilitacion lado izquierdo. |
| Encoder A | Fase A del codificador. |
| Encoder B | Fase B del codificador. |
| CANH/CANL | Bus CAN. |
| 12V | Potencia de motor. |
| GND | Tierra comun. |

## Nodo del elevador con TB6600

El diagrama del Anexo 11.4 muestra un nodo para control de motores paso a paso mediante drivers externos.

Senales principales:

| Senal | Funcion |
|---|---|
| STEP | Pulso de avance de paso. |
| DIR | Direccion de giro. |
| EN | Habilitacion del driver. |
| CANH/CANL | Bus CAN. |
| 12V | Potencia de motor / driver segun implementacion. |
| 5V | Logica. |
| GND | Tierra comun. |

## Pendientes

- Confirmar pines GPIO exactos usados en cada firmware ESP32.
- Subir imagenes originales de los diagramas del Anexo 11.
- Subir fotos reales de cada nodo.
- Confirmar si todos los nodos usan la misma asignacion de pines CAN TX/RX.

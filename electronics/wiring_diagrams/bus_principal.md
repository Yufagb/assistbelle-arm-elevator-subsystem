# Bus principal del robot

Documento generado a partir de la tesis y de la carpeta de Drive de tesis.

## Fuente

- Tesis: Anexo 11.1, diagrama electronico del bus principal.
- Capitulo 5.3.2, arquitectura electronica y distribucion de cableado.

## Lineas principales del bus

El bus principal distribuye simultaneamente potencia y comunicacion hacia los subsistemas del robot.

| Linea | Funcion | Nota |
|---|---|---|
| 12V | Potencia para actuadores | Alimenta drivers y motores. |
| P_GND | Tierra de potencia | Retorno de potencia de actuadores. |
| 5V | Potencia logica | Alimenta Raspberry Pi, ESP32 y logica auxiliar. |
| S_GND | Tierra de senal | Tierra comun de logica y senales. |
| CANH | Linea diferencial CAN alta | Cable trenzado con CANL. |
| CANL | Linea diferencial CAN baja | Cable trenzado con CANH. |

## Conectores vistos en el diagrama

| Bloque | Conector / funcion |
|---|---|
| POWER_SUPPLIES | Entrada/salida de fuente 12V y 5V. |
| RPI_CONNECTIONS | Conexion hacia Raspberry Pi y MCP2515. |
| DC_MOTOR_CONTROLLER | Alimentacion y comunicacion hacia nodos de motores DC. |
| STEPPER_MOTOR_CONTROLLER | Alimentacion y comunicacion hacia nodo del elevador. |

## Terminacion CAN

El diagrama muestra resistencias de terminacion de 120 ohmios en los extremos del bus CAN.

Regla de implementacion:

- colocar 120 ohmios entre CANH y CANL al inicio del bus;
- colocar 120 ohmios entre CANH y CANL al final del bus;
- no colocar terminaciones intermedias en nodos derivados.

## Reglas de cableado documentadas en la tesis

- Potencia para actuadores: 12V y GND con cable 16 AWG.
- Potencia para procesadores: 5V y GND con cable 18 AWG.
- Comunicacion: CANH y CANL con cable 18 AWG trenzado.
- Camara: USB mediante cable USB-C.
- Mantener derivaciones del bus CAN hacia nodos por debajo de 20 cm cuando sea posible.

## Pendiente para cierre HardwareX

- Subir el diagrama original en PDF, PNG o KiCad.
- Confirmar si P_GND y S_GND se unen en un unico punto o en toda la linea.
- Confirmar ubicacion fisica exacta de las resistencias de 120 ohmios.
- Agregar fotografia del bus real y de los conectores usados.

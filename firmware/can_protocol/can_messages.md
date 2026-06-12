# Mensajes CAN del sistema

Documento generado a partir de la tesis, seccion 5.3.3.1 Comunicacion interna.

## Formato general de IDs

La tesis define el formato general:

```text
ID = 0xn00m
```

Donde:

- `n` indica el proposito del mensaje.
- `m` indica el numero de nodo o comando, segun el tipo de mensaje.

## Tipos de mensajes

| Tipo | Direccion | ID base | Funcion |
|---|---|---|---|
| A | Maestro a nodo | 0xA00n | Solicitud de estado. |
| B | Nodo a maestro | 0xB00n | Respuesta de estado. |
| C | Maestro a nodo | 0xC00n | Comando de actuador. |
| D | Maestro a nodo | 0xD00n | Comandos generales. |

## Mensaje A: solicitud de estado

| Campo | Valor |
|---|---|
| ID individual | 0xA00n |
| Broadcast | 0xA006 |
| Emisor | Raspberry Pi |
| Receptor | Nodo especifico o todos los nodos |
| Funcion | Solicitar posicion y velocidad del actuador. |

## Mensaje B: respuesta de estado

| Campo | Valor |
|---|---|
| ID | 0xB00n |
| Emisor | Nodo controlador |
| Receptor | Raspberry Pi |
| Funcion | Enviar posicion y velocidad actuales. |

## Mensaje C: comando de actuador

| Campo | Valor |
|---|---|
| ID | 0xC00n |
| Emisor | Raspberry Pi |
| Receptor | Nodo controlador |
| Funcion | Enviar posicion y velocidad deseadas. |

## Mensaje D: comandos generales

| Comando | Funcion |
|---|---|
| D1 | Cambiar modo de control entre seguimiento de trayectorias y comando directo de velocidad articular. |
| D2 | Comando de efector final; especifica porcentaje de apertura del gripper entre 0 y 100 %. |

## Pendientes

- Confirmar formato exacto de payload por firmware final.
- Confirmar endianness y unidades usadas en bytes.
- Confirmar si J5 usa milimetros, metros o pasos internamente.
- Confirmar si D2 responde solo en el nodo 4 o en otro nodo final.

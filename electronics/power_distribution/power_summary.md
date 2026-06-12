# Resumen de distribucion de potencia

Documento generado a partir de la tesis y de la lista de materiales en Drive.

## Lineas de alimentacion

| Linea | Uso | Cable / nota |
|---|---|---|
| 12 V | Potencia de actuadores y drivers | La tesis indica cable 16 AWG. |
| 5 V | Logica, Raspberry Pi, ESP32 y modulos auxiliares | La tesis indica cable 18 AWG. |
| GND | Tierra comun de potencia y logica | Confirmar punto de union final. |

## Fuente principal

La tesis indica el uso de una fuente principal de 12 V con capacidad de 82 A para alimentar el bus de potencia. Tambien indica el uso de un conversor DC-DC para generar 5 V desde los 12 V para la Raspberry Pi 5 y la logica.

## Componentes relacionados encontrados en Drive

| Componente | Fuente / estado segun lista de materiales |
|---|---|
| Conversor DC-DC 5 A | Pedido online. |
| Raspberry Pi 5 + microSD | Pedido a UTEC. |
| ESP32 DevKitC | Pedido online. |
| Modulos CAN SN65HVD230 | Pedido online. |
| Drivers DRV8871 | Pedido online. |
| NEMA 23 | Pedido online. |
| Baterias LiPo 5200 mAh 11.1 V | Por ordenar en la lista. |
| Cables y jumpers | Pedido a UTEC. |
| Resistencias surtidas | Pedido a UTEC. |

## Pendientes para publicacion

- Confirmar si la implementacion final uso fuente de laboratorio, fuente 12 V 82 A o baterias.
- Confirmar corriente real de cada linea.
- Agregar fusibles o protecciones si existieron.
- Agregar esquema de tierra comun.
- Agregar foto de la distribucion de potencia real.

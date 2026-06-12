# Índice de esquemáticos

Este documento organiza los esquemáticos eléctricos del subsistema de brazo y elevador de Assistbelle.

## Índice

- [Archivos esperados](#archivos-esperados)
- [Criterios de revisión](#criterios-de-revisión)
- [Convención de nombres](#convención-de-nombres)
- [Documentos relacionados](#documentos-relacionados)

## Archivos esperados

| Archivo / grupo | Tipo recomendado | Subsistema | Estado | Observación |
|---|---|---|---|---|
| `system_general.*` | PDF/PNG/KiCad | Sistema completo | Pendiente de confirmación | Debe mostrar Raspberry Pi, MCP2515, CAN, ESP32, drivers y actuadores. |
| `can_bus.*` | PDF/PNG/KiCad | Comunicación | Pendiente de confirmación | Debe mostrar CANH, CANL, GND y terminaciones de 120 ohmios. |
| `power_distribution.*` | PDF/PNG/KiCad | Potencia | Pendiente de confirmación | Debe mostrar 12 V, 5 V, GND, protección y distribución. |
| `esp32_joint_node.*` | PDF/PNG/KiCad | Nodos J1-J4 | Pendiente de confirmación | Debe coincidir con la tabla de pinout ESP32. |
| `j5_tb6600_node.*` | PDF/PNG/KiCad | Elevador J5 | Pendiente de confirmación | Debe mostrar ESP32, TB6600, PUL, DIR, ENA y alimentación del NEMA. |

> Si ya existen archivos con otros nombres, mantenerlos y actualizar esta tabla con enlaces directos.

## Criterios de revisión

Antes de cerrar electrónica para HardwareX, verificar:

- que el diagrama general muestre Raspberry Pi, MCP2515, CANH/CANL, ESP32, drivers y actuadores;
- que exista referencia clara para alimentación de 12 V, 5 V y GND;
- que el bus CAN tenga terminaciones de 120 ohmios en los extremos;
- que los nombres de señales coincidan con los pinouts documentados;
- que cada driver esté asociado al actuador correcto: DRV8871 para motores DC y TB6600 para NEMA/J5;
- que exista al menos una exportación visual PDF/PNG si el archivo editable está en KiCad u otro formato CAD electrónico.

## Convención de nombres

Se recomienda usar nombres en minúscula y descriptivos:

```text
electronics/schematics/system_general.pdf
electronics/schematics/system_general.png
electronics/schematics/can_bus.pdf
electronics/schematics/power_distribution.pdf
electronics/schematics/esp32_joint_node.pdf
electronics/schematics/j5_tb6600_node.pdf
```

## Documentos relacionados

- [`../README.md`](../README.md): mapa general de electrónica.
- [`../pinout_tables/esp32_pinout_table.md`](../pinout_tables/esp32_pinout_table.md): GPIO por nodo ESP32.
- [`../pinout_tables/raspberry_pi_mcp2515.md`](../pinout_tables/raspberry_pi_mcp2515.md): conexión del maestro CAN.
- [`../wiring_diagrams/bus_principal.md`](../wiring_diagrams/bus_principal.md): bus principal de potencia y CAN.
- [`../power_distribution/power_summary.md`](../power_distribution/power_summary.md): distribución de energía.

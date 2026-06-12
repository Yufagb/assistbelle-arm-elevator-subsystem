# Electrónica

Documentación eléctrica y electrónica del subsistema de brazo y elevador de Assistbelle.

## Índice

- [Mapa de carpetas](#mapa-de-carpetas)
- [Estado actual](#estado-actual)
- [Documentos principales](#documentos-principales)
- [Pendientes de cierre](#pendientes-de-cierre)

## Mapa de carpetas

| Carpeta | Contenido | Estado |
|---|---|---|
| [`schematics/`](schematics/) | Esquemáticos eléctricos y exportaciones visuales. | En proceso de cierre |
| [`wiring_diagrams/`](wiring_diagrams/) | Diagramas prácticos de cableado. | Parcial |
| [`pinout_tables/`](pinout_tables/) | Tablas de pines ESP32, Raspberry Pi y módulos CAN. | Avanzado |
| [`power_distribution/`](power_distribution/) | Distribución de potencia, 12 V, 5 V y GND. | Parcial |
| [`images/`](images/) | Fotos o capturas de electrónica. | Pendiente de fotos finales |

## Estado actual

| Bloque | Estado | Referencia |
|---|---|---|
| Pinout ESP32 por nodo | Documentado | [`pinout_tables/esp32_pinout_table.md`](pinout_tables/esp32_pinout_table.md) |
| Raspberry Pi + MCP2515 | Documentado | [`pinout_tables/raspberry_pi_mcp2515.md`](pinout_tables/raspberry_pi_mcp2515.md) |
| Bus principal | Documentado en texto | [`wiring_diagrams/bus_principal.md`](wiring_diagrams/bus_principal.md) |
| Nodos controladores | Documentado en texto | [`wiring_diagrams/nodos_controladores.md`](wiring_diagrams/nodos_controladores.md) |
| Potencia | Resumen inicial | [`power_distribution/power_summary.md`](power_distribution/power_summary.md) |
| Esquemáticos | Subidos o en proceso de indexado | [`schematics/schematics_index.md`](schematics/schematics_index.md) |

## Documentos principales

- [`schematics/README.md`](schematics/README.md)
- [`schematics/schematics_index.md`](schematics/schematics_index.md)
- [`pinout_tables/esp32_pinout_table.md`](pinout_tables/esp32_pinout_table.md)
- [`pinout_tables/raspberry_pi_mcp2515.md`](pinout_tables/raspberry_pi_mcp2515.md)
- [`wiring_diagrams/bus_principal.md`](wiring_diagrams/bus_principal.md)
- [`wiring_diagrams/nodos_controladores.md`](wiring_diagrams/nodos_controladores.md)
- [`power_distribution/power_summary.md`](power_distribution/power_summary.md)

## Pendientes de cierre

- [ ] Confirmar que los esquemáticos subidos cubran sistema general, CAN, potencia y drivers.
- [ ] Exportar cada esquemático editable a PDF/PNG.
- [ ] Agregar fotos reales de electrónica en [`images/`](images/).
- [ ] Crear tabla final de conectores.
- [ ] Verificar consistencia entre esquemáticos, pinouts, firmware y BOM.

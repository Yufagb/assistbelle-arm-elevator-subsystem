# Esquemáticos eléctricos

Esta carpeta contiene los esquemáticos eléctricos del subsistema de brazo y elevador de Assistbelle.

## Índice

- [Archivos disponibles](schematics_index.md)
- [Criterios mínimos](#criterios-mínimos)
- [Revisión recomendada](#revisión-recomendada)
- [Documentos relacionados](#documentos-relacionados)

## Archivos disponibles

El índice principal vive en:

```text
electronics/schematics/schematics_index.md
```

Abrir aquí: [`schematics_index.md`](schematics_index.md).

## Criterios mínimos

Para que un esquemático se considere listo para publicación, debe permitir identificar:

- alimentación principal;
- conversión o distribución de 12 V y 5 V;
- tierra común entre lógica, drivers y bus;
- conexión CANH/CANL;
- nodo maestro Raspberry Pi + MCP2515;
- nodos ESP32;
- drivers DRV8871 para motores DC;
- driver TB6600 para el eje J5/NEMA;
- actuadores, gripper y señales auxiliares.

## Revisión recomendada

Antes del envío final:

- exportar PDF o PNG de cada esquemático editable;
- confirmar nombres de señales contra los pinouts;
- confirmar corriente máxima de drivers y actuadores;
- añadir terminaciones CAN de 120 ohmios si no están explícitas;
- revisar conectores físicos y numeración de pines;
- añadir fecha o versión del diagrama.

## Documentos relacionados

- [`../README.md`](../README.md)
- [`schematics_index.md`](schematics_index.md)
- [`../pinout_tables/esp32_pinout_table.md`](../pinout_tables/esp32_pinout_table.md)
- [`../pinout_tables/raspberry_pi_mcp2515.md`](../pinout_tables/raspberry_pi_mcp2515.md)
- [`../wiring_diagrams/bus_principal.md`](../wiring_diagrams/bus_principal.md)
- [`../wiring_diagrams/nodos_controladores.md`](../wiring_diagrams/nodos_controladores.md)
- [`../power_distribution/power_summary.md`](../power_distribution/power_summary.md)

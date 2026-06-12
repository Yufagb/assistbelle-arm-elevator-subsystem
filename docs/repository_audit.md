# Auditoria de avance del repositorio

Este documento resume el estado de la rama `hardwarex-publication-package` y las mejoras pendientes antes de preparar el manuscrito.

## Estado general

| Area | Estado | Ubicacion |
|---|---|---|
| Estructura general | Avanzada | `README.md`, `docs/repository_structure.md` |
| Documentacion | Avanzada | `docs/` |
| Firmware ESP32 | Avanzado | `firmware/` |
| ROS 2 | Avanzado | `ros2_ws/` |
| Electronica | Parcial | `electronics/` |
| BOM | Inicial completa | `docs/bom_template.csv` |
| CAD y mecanica | Pendiente critico | `hardware/` |
| Validacion | Pendiente de curado | `validation/` |
| Paper | Pendiente | `paper/` |
| Licencias | Pendiente | `docs/license_overview.md` |

## Avances confirmados

### Firmware

- Los proyectos ESP-IDF J1, J2, J3, J4 y J5 estan migrados a `firmware/`.
- Los pines de ESP32 estan documentados en `electronics/pinout_tables/esp32_pinout_table.md`.
- El nodo J5 final queda documentado con TB6600.
- DRV8871 queda documentado como driver de motores DC.
- ESP-IDF queda fuera del repositorio como dependencia externa.

### ROS 2

- El paquete `can_comm_pkg` compila localmente.
- `can_node` inicia correctamente cuando existe una interfaz `can0` virtual.
- Los artefactos generados de ROS 2 e IDE fueron retirados del versionado.

### Electronica

- La conexion Raspberry Pi a MCP2515 esta documentada.
- El bus principal esta documentado en texto.
- Los nodos controladores estan relacionados con actuadores y drivers.

### BOM

- La lista de materiales fue convertida a CSV ordenado.
- Se retiraron componentes no usados: Astra, Astra Plus, bateria LiPo, tablet y DRV8825.
- Se agregaron precios referenciales a componentes provistos institucionalmente.
- Se separo el uso final de drivers: DRV8871 para motores DC y TB6600 para NEMA23.

## Pendientes prioritarios

1. Probar los entry points principales de ROS 2: `control_teclado`, `can_traj`, `can_slider` e `ik_node`.
2. Mover evidencias seleccionadas desde `resultados/` hacia `validation/`.
3. Crear un indice de videos y resultados en `validation/media/`.
4. Completar diagramas electricos finales en `electronics/`.
5. Completar CAD, STEP, STL y planos cuando el CAD este disponible.
6. Crear `LICENSE` y `CITATION.cff`.
7. Preparar figuras y tablas para `paper/`.
8. Traducir documentacion clave al ingles tecnico antes del envio.

## Reglas de orden

- `ros2_ws/` contiene solo workspace ROS 2.
- `firmware/` contiene firmware ESP32 final.
- `electronics/` contiene pinouts, cableado, potencia, esquematicos e imagenes electricas.
- `hardware/` contiene CAD, STEP, STL, planos, fotos y fasteners.
- `resultados/` queda como evidencia bruta.
- `validation/` contiene evidencia curada para publicacion.
- `paper/` contiene elementos del manuscrito.

## Criterio de cierre

La rama estara lista para comenzar el manuscrito cuando:

- Firmware J1-J5 compile desde un clon limpio.
- ROS 2 compile desde un clon limpio.
- `can_node` funcione con `can0` virtual y luego con CAN fisico.
- La BOM tenga componentes finales y costos revisados.
- La electronica tenga diagramas suficientes para replicacion.
- La validacion tenga videos, datos y figuras curadas.
- La mecanica tenga CAD/STEP/STL o se declare claramente como pendiente critico.

# Auditoría de avance del repositorio

Este documento resume el estado del repositorio público `assistbelle-arm-elevator-subsystem` y las mejoras pendientes antes del manuscrito.

## Índice

- [Estado general](#estado-general)
- [Avances confirmados](#avances-confirmados)
- [Pendientes prioritarios](#pendientes-prioritarios)
- [Criterio de cierre](#criterio-de-cierre)

## Estado general

| Área | Estado | Ubicación |
|---|---|---|
| Estructura general | Avanzada | [`../README.md`](../README.md), [`repository_structure.md`](repository_structure.md) |
| Documentación | Avanzada | [`./`](./) |
| Firmware ESP32 | Avanzado | [`../firmware/`](../firmware/) |
| ROS 2 | Avanzado | [`../ros2_ws/`](../ros2_ws/) |
| Electrónica | Parcial avanzada | [`../electronics/`](../electronics/) |
| Esquemáticos | En proceso de cierre | [`../electronics/schematics/schematics_index.md`](../electronics/schematics/schematics_index.md) |
| BOM | Inicial completa | [`bom_template.csv`](bom_template.csv) |
| CAD y mecánica | Pendiente crítico | [`../hardware/`](../hardware/) |
| Validación | Estructura lista | [`../validation/`](../validation/) |
| Paper | Pendiente | [`../paper/`](../paper/) |
| Licencias | Inicial listo | [`../LICENSE`](../LICENSE), [`../CITATION.cff`](../CITATION.cff) |

## Avances confirmados

### Firmware

- Proyectos ESP-IDF J1, J2, J3, J4 y J5 migrados a `firmware/`.
- J5 documentado con TB6600.
- DRV8871 documentado como driver de motores DC.
- ESP-IDF queda fuera del repositorio como dependencia externa.

### ROS 2

- `can_comm_pkg` compila localmente.
- `can_node` inicia con `can0` virtual.
- Entry points principales documentados para validación.

### Electrónica

- Raspberry Pi + MCP2515 documentado.
- Bus principal documentado en texto.
- Nodos controladores relacionados con actuadores y drivers.
- Carpeta de esquemáticos activa y con índice.
- Falta cerrar fotos, conectores y revisión cruzada con firmware.

### BOM

- BOM convertida a CSV ordenado.
- Componentes no usados retirados: Astra, Astra Plus, batería LiPo, tablet y DRV8825.
- Precios referenciales agregados.
- Drivers finales separados: DRV8871 para DC y TB6600 para NEMA23/J5.

## Pendientes prioritarios

1. Revisar e indexar esquemáticos finales.
2. Probar entry points ROS 2.
3. Mover o enlazar evidencias seleccionadas hacia `validation/`.
4. Crear figuras finales de validación.
5. Completar tabla de conectores y fotos de electrónica.
6. Completar CAD, STEP, STL y planos.
7. Preparar figuras/tablas para `paper/`.
8. Traducir documentación clave al inglés técnico.

## Criterio de cierre

El repositorio estará listo para comenzar el manuscrito cuando:

- firmware J1-J5 compile desde un clon limpio;
- ROS 2 compile desde un clon limpio;
- `can_node` funcione con CAN virtual y físico;
- electrónica tenga esquemáticos, pinouts, conectores y fotos suficientes;
- BOM esté revisada;
- validación tenga videos, datos y figuras curadas;
- mecánica tenga CAD/STEP/STL o se declare claramente como pendiente crítico.

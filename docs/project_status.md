# Estado actual del proyecto HardwareX

Este documento resume el estado real del repositorio público `assistbelle-arm-elevator-subsystem`.

## Índice

- [Resumen ejecutivo](#resumen-ejecutivo)
- [Estado por área](#estado-por-área)
- [BOM activa](#bom-activa)
- [Pendientes inmediatos](#pendientes-inmediatos)
- [Criterio de cierre para HardwareX](#criterio-de-cierre-para-hardwarex)

## Resumen ejecutivo

El repositorio ya tiene una estructura ordenada para publicación tipo HardwareX. Se separan correctamente ROS 2, firmware ESP32, electrónica, hardware mecánico, validación, documentación y material del paper.

El firmware ESP32 J1-J5 compila localmente. ROS 2 compila localmente para `can_comm_pkg`, y `can_node` inicia con una interfaz `can0` virtual usando SocketCAN/vcan.

La BOM HardwareX del elevador fue sincronizada con el Google Sheet `ASM_Elevator_System_HardwareX_BOM`, pestaña `BOM_Final_Clean`, asociada al CAD v54. Incluye estructura, actuación, guías, fasteners y electrónica CAD: Raspberry Pi 5, MCP2515 CAN-SPI y dos drivers TB6600. La BOM anterior `docs/bom_template.csv` se conserva como referencia histórica/continuidad, pero la BOM limpia para publicación del elevador está en `docs/bom/hardwarex_elevator_bom_final.csv`.

## Estado por área

| Área | Estado | Observación |
|---|---|---|
| Estructura del repo | Avanzada | Ver [`repository_structure.md`](repository_structure.md). |
| README principal | Avanzado | Con navegación interna, BOM v54 sincronizada y enlaces funcionales. |
| Firmware J1-J4 | Compila localmente | [`../firmware/esp32_joint_node/`](../firmware/esp32_joint_node/) |
| Firmware J5 | Compila localmente | [`../firmware/esp32_stepper_node/J5_tb6600/`](../firmware/esp32_stepper_node/J5_tb6600/) |
| Pinout ESP32 | Documentado | [`../electronics/pinout_tables/esp32_pinout_table.md`](../electronics/pinout_tables/esp32_pinout_table.md) |
| Raspberry Pi/MCP2515 | Documentado e incluido en BOM/CAD | [`../electronics/pinout_tables/raspberry_pi_mcp2515.md`](../electronics/pinout_tables/raspberry_pi_mcp2515.md), [`bom/hardwarex_elevator_bom_final.md`](bom/hardwarex_elevator_bom_final.md) |
| Bus principal | Documentado en texto | [`../electronics/wiring_diagrams/bus_principal.md`](../electronics/wiring_diagrams/bus_principal.md) |
| Esquemáticos | En proceso de cierre | [`../electronics/schematics/schematics_index.md`](../electronics/schematics/schematics_index.md) |
| Protocolo CAN | Documentado | [`../firmware/can_protocol/can_messages.md`](../firmware/can_protocol/can_messages.md) |
| ROS 2 | Compila e inicia con vcan | Falta probar todos los entry points. |
| BOM | Sincronizada con Google Sheet / CAD v54 | [`bom/hardwarex_elevator_bom_final.md`](bom/hardwarex_elevator_bom_final.md), 32 ítems + total estimado. |
| Licencia/citación | Inicial listo | [`../LICENSE`](../LICENSE), [`../CITATION.cff`](../CITATION.cff) |
| CAD/STEP/STL | Pendiente crítico | Falta contenido mecánico final. |
| Validación | Estructura lista | Falta copiar/enlazar evidencias. |
| Paper | Pendiente | Carpeta creada, falta manuscrito. |

## BOM activa

La BOM limpia para publicación HardwareX del elevador está en:

```text
docs/bom/hardwarex_elevator_bom_final.csv
```

La versión legible en GitHub está en:

```text
docs/bom/hardwarex_elevator_bom_final.md
```

Trazabilidad de la BOM:

```text
docs/bom/README.md
```

Resumen actual:

- 32 ítems de BOM + 1 fila de total estimado.
- Fuente: Google Sheet `ASM_Elevator_System_HardwareX_BOM`, tab `BOM_Final_Clean`.
- CAD asociado en la fuente: `ASM_Elevator_System.step` + `ASM_Elevator_System.f3z`, release v54.
- Moneda: USD estimados.
- Total estimado de producto/material: USD 484.78.
- No incluye envío, aduanas, impuestos ni cambios de precio de marketplace.
- Raspberry Pi 5 conserva costo estimado hasta confirmar vendedor/producto exacto.
- `docs/bom_template.csv` se conserva solo como referencia anterior en formato español/PEN.

El costo estimado es preliminar y debe revisarse antes de publicación/compra final.

## Pendientes inmediatos

1. Confirmar los nombres finales y exportaciones de esquemáticos.
2. Probar entry points principales de ROS 2:

```bash
ros2 run can_comm_pkg control_teclado
ros2 run can_comm_pkg can_traj
ros2 run can_comm_pkg can_slider
ros2 run can_comm_pkg ik_node
ros2 run can_comm_pkg j5_ramp
ros2 run can_comm_pkg j5_trap
```

3. Verificar que no haya artefactos versionados:

```bash
git ls-files | grep -E '(^|/)(build|install|log|\.idea|\.vscode)(/|$)'
```

4. Completar fotos y tabla final de conectores en electrónica.
5. Completar CAD/STEP/STL en `hardware/`.
6. Curar videos y datos hacia `validation/`.
7. Re-exportar `docs/bom/hardwarex_elevator_bom_final.csv` si cambia el Google Sheet fuente o el CAD agrega componentes.

## Criterio de cierre para HardwareX

La versión estará lista para manuscrito cuando:

- firmware J1-J5 compile desde un clon limpio;
- ROS 2 compile desde un clon limpio;
- `can_node` funcione con CAN virtual y físico;
- electrónica tenga esquemáticos, pinouts, conectores y fotos suficientes;
- la BOM permita comprar o sustituir componentes;
- validación tenga datos, videos y figuras curadas;
- mecánica tenga CAD/STEP/STL o se declare como pendiente crítico.

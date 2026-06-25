<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Documentación del proyecto

Esta carpeta concentra la documentación general del paquete HardwareX de Assistbelle.

## Índice

- [Lectura recomendada](#lectura-recomendada)
- [Archivos principales](#archivos-principales)
- [Relación con otras carpetas](#relación-con-otras-carpetas)
- [Estado actual](#estado-actual)
- [Criterios de documentación](#criterios-de-documentación)

## Lectura recomendada

1. [`project_status.md`](project_status.md): estado actual del repositorio.
2. [`repository_audit.md`](repository_audit.md): auditoría de avance y pendientes.
3. [`repo_cleanup_audit.md`](repo_cleanup_audit.md): auditoría de limpieza, placeholders y archivos generados.
4. [`repository_structure.md`](repository_structure.md): reglas de organización.
5. [`hardwarex_master_checklist.md`](hardwarex_master_checklist.md): checklist maestro.
6. [`publication_checklist.md`](publication_checklist.md): checklist de publicación.
7. [`operation_manual.md`](operation_manual.md): operación básica y comandos.
8. [`ros2_entrypoints_validation.md`](ros2_entrypoints_validation.md): validación de comandos ROS 2.
9. [`calibration_manual.md`](calibration_manual.md): calibración.
10. [`safety_notes.md`](safety_notes.md): seguridad.
11. [`troubleshooting.md`](troubleshooting.md): problemas comunes.
12. [`bom/README.md`](bom/README.md): índice de BOM HardwareX.
13. [`bom/hardwarex_elevator_bom_final.md`](bom/hardwarex_elevator_bom_final.md): BOM legible para revisión.
14. [`bom/hardwarex_elevator_bom_final.csv`](bom/hardwarex_elevator_bom_final.csv): BOM machine-readable.
15. [`procurement/README.md`](procurement/README.md): compras y evidencia pública curada.
16. [`license_overview.md`](license_overview.md): licencias y citación.

## Archivos principales

| Archivo | Propósito |
|---|---|
| [`project_status.md`](project_status.md) | Estado real del proyecto por área. |
| [`repository_audit.md`](repository_audit.md) | Revisión general, pendientes y criterio de cierre. |
| [`repo_cleanup_audit.md`](repo_cleanup_audit.md) | Auditoría de limpieza del repo y comandos locales de validación. |
| [`repository_structure.md`](repository_structure.md) | Reglas de carpetas y migración. |
| [`hardwarex_master_checklist.md`](hardwarex_master_checklist.md) | Checklist de cierre HardwareX. |
| [`publication_checklist.md`](publication_checklist.md) | Checklist extendido de publicación. |
| [`operation_manual.md`](operation_manual.md) | Secuencia de compilación, CAN y ejecución. |
| [`calibration_manual.md`](calibration_manual.md) | Calibración inicial. |
| [`safety_notes.md`](safety_notes.md) | Seguridad del prototipo. |
| [`troubleshooting.md`](troubleshooting.md) | Solución de errores comunes. |
| [`ros2_entrypoints_validation.md`](ros2_entrypoints_validation.md) | Pruebas de entry points ROS 2. |
| [`bom/README.md`](bom/README.md) | Índice de BOM, trazabilidad y orden de lectura. |
| [`bom/hardwarex_elevator_bom_final.md`](bom/hardwarex_elevator_bom_final.md) | BOM HardwareX legible para GitHub. |
| [`bom/hardwarex_elevator_bom_final.csv`](bom/hardwarex_elevator_bom_final.csv) | BOM HardwareX completa en CSV. |
| [`procurement/README.md`](procurement/README.md) | Política pública de evidencia de compras. |
| [`procurement/purchase_log_public.csv`](procurement/purchase_log_public.csv) | Log público y curado de compras/procurement. |
| [`license_overview.md`](license_overview.md) | Licencias, `LICENSE` y `CITATION.cff`. |

## Relación con otras carpetas

| Carpeta | Documentación relacionada |
|---|---|
| [`../firmware/`](../firmware/) | [`../firmware/README.md`](../firmware/README.md), [`../firmware/ESP_IDF_BUILD_GUIDE.md`](../firmware/ESP_IDF_BUILD_GUIDE.md), [`../firmware/can_protocol/can_messages.md`](../firmware/can_protocol/can_messages.md) |
| [`../electronics/`](../electronics/) | [`../electronics/README.md`](../electronics/README.md), [`../electronics/schematics/schematics_index.md`](../electronics/schematics/schematics_index.md), [`../electronics/pinout_tables/esp32_pinout_table.md`](../electronics/pinout_tables/esp32_pinout_table.md), [`../electronics/wiring_diagrams/connector_table.md`](../electronics/wiring_diagrams/connector_table.md) |
| [`../ros2_ws/`](../ros2_ws/) | Workspace ROS 2 y paquete `can_comm_pkg`. |
| [`../hardware/`](../hardware/) | [`../hardware/README.md`](../hardware/README.md), [`../hardware/design_files_index.md`](../hardware/design_files_index.md) y subcarpetas CAD/STEP/STL/drawings. |
| [`../validation/`](../validation/) | [`../validation/validation_plan.md`](../validation/validation_plan.md) y evidencias curadas. |
| [`../paper/`](../paper/) | [`../paper/manuscript_outline.md`](../paper/manuscript_outline.md), [`../paper/data_availability_statement.md`](../paper/data_availability_statement.md), figuras y tablas del manuscrito. |

## Estado actual

- Firmware ESP32 J1-J5 migrado e incluido.
- Pinout ESP32 documentado.
- Protocolo CAN documentado; `C5` es compatible con ROS 2 y `B5` queda pendiente de cierre físico/firmware.
- Raspberry Pi + MCP2515 documentado.
- ROS 2 compila localmente y `can_node` inicia con `can0` virtual; falta clean-clone entry-point validation.
- BOM HardwareX activa: 32 ítems + total estimado USD 484.78.
- Evidencia pública de compras creada en [`procurement/`](procurement/).
- Esquemáticos y electrónica documentados en texto; fotos y verificación física de conectores quedan pendientes.
- CAD/STEP/STL/PDF/DXF mecánicos del snapshot v60 cargados; fotos físicas del robot quedan diferidas.
- Manuscript outline, data availability statement, design-files table, BOM table y diagramas Mermaid draft creados en [`../paper/`](../paper/).

## Criterios de documentación

- No duplicar información técnica si puede enlazarse.
- Mantener ROS 2 dentro de [`../ros2_ws/`](../ros2_ws/).
- Mantener firmware ESP32 dentro de [`../firmware/`](../firmware/).
- Mantener electrónica en [`../electronics/`](../electronics/).
- Mantener mecánica en [`../hardware/`](../hardware/).
- Mantener evidencias curadas en [`../validation/`](../validation/).
- Mantener comprobantes brutos o documentos financieros fuera del repositorio público salvo que estén revisados y redactados.
- Antes del envío final, traducir documentación clave al inglés técnico.

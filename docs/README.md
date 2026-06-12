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
3. [`repository_structure.md`](repository_structure.md): reglas de organización.
4. [`hardwarex_master_checklist.md`](hardwarex_master_checklist.md): checklist maestro.
5. [`operation_manual.md`](operation_manual.md): operación básica y comandos.
6. [`ros2_entrypoints_validation.md`](ros2_entrypoints_validation.md): validación de comandos ROS 2.
7. [`calibration_manual.md`](calibration_manual.md): calibración.
8. [`safety_notes.md`](safety_notes.md): seguridad.
9. [`troubleshooting.md`](troubleshooting.md): problemas comunes.
10. [`bom_template.csv`](bom_template.csv): lista de materiales.
11. [`license_overview.md`](license_overview.md): licencias y citación.

## Archivos principales

| Archivo | Propósito |
|---|---|
| [`project_status.md`](project_status.md) | Estado real del proyecto por área. |
| [`repository_audit.md`](repository_audit.md) | Revisión general, pendientes y criterio de cierre. |
| [`repository_structure.md`](repository_structure.md) | Reglas de carpetas y migración. |
| [`hardwarex_master_checklist.md`](hardwarex_master_checklist.md) | Checklist de cierre HardwareX. |
| [`publication_checklist.md`](publication_checklist.md) | Checklist extendido de publicación. |
| [`operation_manual.md`](operation_manual.md) | Secuencia de compilación, CAN y ejecución. |
| [`calibration_manual.md`](calibration_manual.md) | Calibración inicial. |
| [`safety_notes.md`](safety_notes.md) | Seguridad del prototipo. |
| [`troubleshooting.md`](troubleshooting.md) | Solución de errores comunes. |
| [`ros2_entrypoints_validation.md`](ros2_entrypoints_validation.md) | Pruebas de entry points ROS 2. |
| [`bom_template.csv`](bom_template.csv) | BOM activa con costos y proveedores. |
| [`license_overview.md`](license_overview.md) | Licencias, `LICENSE` y `CITATION.cff`. |

## Relación con otras carpetas

| Carpeta | Documentación relacionada |
|---|---|
| [`../firmware/`](../firmware/) | [`../firmware/README.md`](../firmware/README.md), [`../firmware/ESP_IDF_BUILD_GUIDE.md`](../firmware/ESP_IDF_BUILD_GUIDE.md), [`../firmware/can_protocol/can_messages.md`](../firmware/can_protocol/can_messages.md) |
| [`../electronics/`](../electronics/) | [`../electronics/README.md`](../electronics/README.md), [`../electronics/schematics/schematics_index.md`](../electronics/schematics/schematics_index.md), [`../electronics/pinout_tables/esp32_pinout_table.md`](../electronics/pinout_tables/esp32_pinout_table.md) |
| [`../ros2_ws/`](../ros2_ws/) | Workspace ROS 2 y paquete `can_comm_pkg`. |
| [`../hardware/`](../hardware/) | [`../hardware/README.md`](../hardware/README.md) y subcarpetas CAD/STEP/STL. |
| [`../validation/`](../validation/) | [`../validation/validation_plan.md`](../validation/validation_plan.md) y evidencias curadas. |
| [`../paper/`](../paper/) | Figuras, tablas y referencias del manuscrito. |

## Estado actual

- Firmware ESP32 J1-J5 migrado y compilado localmente.
- Pinout ESP32 documentado.
- Protocolo CAN documentado.
- Raspberry Pi + MCP2515 documentado.
- ROS 2 compila localmente y `can_node` inicia con `can0` virtual.
- BOM activa actualizada con 38 líneas.
- Esquemáticos subidos o en proceso de indexado.
- CAD/STEP/STL, validación curada y manuscrito siguen pendientes.

## Criterios de documentación

- No duplicar información técnica si puede enlazarse.
- Mantener ROS 2 dentro de [`../ros2_ws/`](../ros2_ws/).
- Mantener firmware ESP32 dentro de [`../firmware/`](../firmware/).
- Mantener electrónica en [`../electronics/`](../electronics/).
- Mantener mecánica en [`../hardware/`](../hardware/).
- Mantener evidencias curadas en [`../validation/`](../validation/).
- Antes del envío final, traducir documentación clave al inglés técnico.

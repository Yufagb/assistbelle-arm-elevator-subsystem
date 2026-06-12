# Documentacion del proyecto

Esta carpeta concentra la documentacion general de la rama `hardwarex-publication-package`.

La documentacion esta organizada para preparar el repositorio como paquete reproducible: operacion, calibracion, seguridad, troubleshooting, estructura, estado del proyecto, checklist, lista de materiales y licencias.

## Lectura recomendada

1. `project_status.md`: estado actual del repositorio y pendientes principales.
2. `repository_structure.md`: reglas de organizacion de carpetas.
3. `hardwarex_master_checklist.md`: checklist maestro para cierre HardwareX.
4. `operation_manual.md`: operacion basica del sistema.
5. `calibration_manual.md`: calibracion inicial de articulaciones y subsistemas.
6. `safety_notes.md`: notas de seguridad para uso en laboratorio.
7. `troubleshooting.md`: errores conocidos y soluciones.
8. `bom_template.csv`: plantilla de lista de materiales.
9. `license_overview.md`: propuesta de licencias por tipo de archivo.

## Archivos principales

| Archivo | Proposito |
|---|---|
| `project_status.md` | Resume el estado real del proyecto, incluyendo firmware, electronica, ROS 2, CAD, BOM y validacion. |
| `repository_structure.md` | Define donde debe ir cada tipo de archivo para evitar duplicados. |
| `hardwarex_master_checklist.md` | Lista de verificacion para saber que falta antes de enviar a revista. |
| `publication_checklist.md` | Checklist extendido de preparacion de publicacion. |
| `operation_manual.md` | Secuencia general de uso del robot. |
| `calibration_manual.md` | Pasos de calibracion y verificacion. |
| `safety_notes.md` | Reglas de seguridad del prototipo. |
| `troubleshooting.md` | Problemas reales encontrados y como resolverlos. |
| `bom_template.csv` | Plantilla para completar la lista de materiales. |
| `license_overview.md` | Resumen de licencias recomendadas para software, hardware y documentacion. |

## Relacion con otras carpetas

| Carpeta | Documentacion relacionada |
|---|---|
| `firmware/` | `firmware/README.md`, `firmware/ESP_IDF_BUILD_GUIDE.md`, `firmware/can_protocol/can_messages.md`. |
| `electronics/` | `electronics/README.md`, `electronics/pinout_tables/esp32_pinout_table.md`, `electronics/wiring_diagrams/bus_principal.md`. |
| `ros2_ws/` | `ros2_ws/src/can_comm_pkg/can_comm_pkg/core/README.md` y `ros2_ws/src/can_comm_pkg/can_comm_pkg/apps/README.md`. |
| `hardware/` | `hardware/README.md` y README internos de CAD, STEP, STL, planos y fotos. |
| `validation/` | README internos de pruebas articulares, cinematica, percepcion, pick-and-place, figuras y media. |
| `paper/` | README de figuras, tablas y referencias del manuscrito. |

## Estado actual

- Firmware ESP32 J1-J5 migrado a `firmware/` y compilado localmente.
- Pinout ESP32 documentado.
- Protocolo CAN documentado.
- Conexion Raspberry Pi a MCP2515 documentada.
- Bus principal documentado parcialmente.
- ROS 2 compila localmente; la ejecucion de `can_node` requiere `can0` fisico o virtual.
- CAD, STEP, STL, BOM final y datasets curados siguen pendientes.

## Criterios de documentacion

- No duplicar informacion tecnica en varias carpetas si puede enlazarse.
- Mantener ROS 2 dentro de `ros2_ws/`.
- Mantener firmware ESP32 dentro de `firmware/`.
- Mantener datos brutos en `resultados/` y datos curados en `validation/`.
- Mantener evidencia mecanica en `hardware/` y evidencia electronica en `electronics/`.
- Antes del envio final, traducir la documentacion principal al ingles tecnico.

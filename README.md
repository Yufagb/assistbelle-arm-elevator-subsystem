<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Assistbelle / Robot asistivo 5-DOF

Repositorio público de preparación para publicación tipo **HardwareX** de un manipulador robótico asistivo de 5 grados de libertad, orientado a tareas de laboratorio para traslado y manipulación de implementos médicos en un entorno controlado.

El sistema integra **ROS 2**, **bus CAN / SocketCAN**, **ESP32 + ESP-IDF**, nodos distribuidos por articulación, drivers **DRV8871** para motores DC y **TB6600** para el eje prismático/elevador.

> Este repositorio público usa `main` como rama principal. Fue generado a partir de la rama de preparación `hardwarex-publication-package` del repositorio histórico `robot-project`.

## Índice rápido

- [Descripción del sistema](#descripción-del-sistema)
- [Quick start](#quick-start)
- [Estado actual](#estado-actual)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Documentación principal](#documentación-principal)
- [Firmware ESP32](#firmware-esp32)
- [ROS 2](#ros-2)
- [Electrónica](#electrónica)
- [Hardware mecánico](#hardware-mecánico)
- [Validación](#validación)
- [Lista de materiales](#lista-de-materiales)
- [License](#license)
- [Checklist de cierre](#checklist-de-cierre)
- [Enfoque recomendado del artículo](#enfoque-recomendado-del-artículo)

## Descripción del sistema

Assistbelle es un subsistema de brazo y elevador para un robot asistivo. El paquete documenta el diseño reproducible del manipulador, la electrónica de control, el firmware distribuido y la capa ROS 2 usada para enviar comandos por CAN.

| Módulo | Descripción |
|---|---|
| Manipulador | Brazo robótico con articulaciones rotativas y gripper. |
| Elevador | Eje prismático J5 accionado con motor NEMA y driver TB6600. |
| Control principal | ROS 2 sobre computador principal o Raspberry Pi. |
| Control distribuido | Nodos ESP32 con ESP-IDF por articulación. |
| Comunicación | Bus CAN mediante SocketCAN. |
| Documentación | README, manuales, pinouts, BOM, validación y checklist HardwareX. |

## Quick start

Este flujo permite verificar rápidamente el paquete ROS 2 y el nodo CAN usando una interfaz CAN virtual (`vcan`).

```bash
git clone https://github.com/Yufagb/assistbelle-arm-elevator-subsystem.git
cd assistbelle-arm-elevator-subsystem/ros2_ws
source /opt/ros/jazzy/setup.bash
pip install -r ../requirements.txt
rm -rf build install log
colcon build --packages-select can_comm_pkg
source install/setup.bash
sudo modprobe vcan
sudo ip link add dev can0 type vcan 2>/dev/null || true
sudo ip link set up can0
ros2 run can_comm_pkg can_node
```

Salida esperada del nodo CAN:

```text
CANNode iniciado y suscrito a /can_command
```

Para firmware ESP32, usar la guía específica: [`firmware/ESP_IDF_BUILD_GUIDE.md`](firmware/ESP_IDF_BUILD_GUIDE.md).

## Estado actual

| Área | Estado | Evidencia / ubicación |
|---|---|---|
| Estructura del repositorio | Avanzada | [`docs/repository_structure.md`](docs/repository_structure.md), [`docs/repository_audit.md`](docs/repository_audit.md) |
| Firmware ESP32 J1-J4 | Compila localmente | [`firmware/esp32_joint_node/`](firmware/esp32_joint_node/) |
| Firmware ESP32 J5/TB6600 | Compila localmente | [`firmware/esp32_stepper_node/J5_tb6600/`](firmware/esp32_stepper_node/J5_tb6600/) |
| ROS 2 | Compila e inicia con `vcan` | [`ros2_ws/`](ros2_ws/), [`docs/ros2_entrypoints_validation.md`](docs/ros2_entrypoints_validation.md) |
| CAN virtual | Validado localmente | `can_node` inicia con `can0` virtual. |
| Pinouts ESP32 | Documentados | [`electronics/pinout_tables/esp32_pinout_table.md`](electronics/pinout_tables/esp32_pinout_table.md) |
| Raspberry Pi + MCP2515 | Documentado | [`electronics/pinout_tables/raspberry_pi_mcp2515.md`](electronics/pinout_tables/raspberry_pi_mcp2515.md) |
| Protocolo CAN | Documentado | [`firmware/can_protocol/can_messages.md`](firmware/can_protocol/can_messages.md) |
| BOM | Inicial completa | [`docs/bom_template.csv`](docs/bom_template.csv) |
| Esquemáticos | En proceso de cierre | [`electronics/schematics/`](electronics/schematics/) |
| Validación | Estructura lista | [`validation/validation_plan.md`](validation/validation_plan.md), [`validation/media/media_index.md`](validation/media/media_index.md) |
| Licencia y citación | Multi-licencia inicial lista | [`LICENSE`](LICENSE), [`LICENSES/`](LICENSES/), [`CITATION.cff`](CITATION.cff) |
| CAD/STEP/STL | Pendiente crítico | [`hardware/`](hardware/) |
| Paper | Pendiente | [`paper/`](paper/) |

## Estructura del repositorio

```text
assistbelle-arm-elevator-subsystem/
├── README.md
├── LICENSE
├── LICENSES/
├── CITATION.cff
├── requirements.txt
├── docs/
├── electronics/
├── firmware/
├── hardware/
├── paper/
├── ros2_ws/
├── software/
└── validation/
```

| Carpeta / archivo | Estado | Propósito |
|---|---|---|
| [`LICENSE`](LICENSE) | Activo | Resumen de la política multi-licencia. |
| [`LICENSES/`](LICENSES/) | Activo | Textos de licencias por tipo de contenido. |
| [`docs/`](docs/) | Activo | Estado, manuales, auditoría, checklist, BOM, seguridad y operación. |
| [`electronics/`](electronics/) | Activo | Pinouts, cableado, potencia, esquemáticos e imágenes de electrónica. |
| [`firmware/`](firmware/) | Activo | Firmware ESP32 organizado por nodo. |
| [`hardware/`](hardware/) | Pendiente de contenido final | CAD, STEP, STL, planos, fotos mecánicas y fasteners. |
| [`paper/`](paper/) | Pendiente de manuscrito | Figuras, tablas, referencias y archivos del artículo. |
| [`ros2_ws/`](ros2_ws/) | Activo | Workspace ROS 2 completo del proyecto. |
| [`software/`](software/) | Auxiliar | Guías de instalación y scripts no ROS 2. |
| [`validation/`](validation/) | Activo | Datos curados, tablas, figuras y evidencias de validación. |

### Carpetas no recomendadas en la versión pública

| Carpeta | Acción |
|---|---|
| `Codigo_esp32/` | No usar como carpeta final; migrar código útil a [`firmware/`](firmware/). |
| `resultados/` | No usar como dataset final; curar evidencias hacia [`validation/`](validation/). |
| `.vscode/`, `.idea/`, `build/`, `install/`, `log/` | No versionar. |
| `hardware/CAD_editable/`, `hardware/STEP/`, `hardware/STL/` | Usar carpetas canónicas en minúsculas: [`hardware/cad/`](hardware/cad/), [`hardware/step/`](hardware/step/), [`hardware/stl/`](hardware/stl/). |

## Documentación principal

| Documento | Descripción |
|---|---|
| [`docs/README.md`](docs/README.md) | Índice general de documentación. |
| [`docs/project_status.md`](docs/project_status.md) | Estado actual del proyecto y pendientes principales. |
| [`docs/repository_audit.md`](docs/repository_audit.md) | Auditoría de avance y criterio de cierre. |
| [`docs/repository_structure.md`](docs/repository_structure.md) | Reglas de organización de carpetas. |
| [`docs/hardwarex_master_checklist.md`](docs/hardwarex_master_checklist.md) | Checklist maestro para cerrar el paquete. |
| [`docs/operation_manual.md`](docs/operation_manual.md) | Operación con ROS 2, SocketCAN y ESP-IDF. |
| [`docs/calibration_manual.md`](docs/calibration_manual.md) | Guía inicial de calibración. |
| [`docs/safety_notes.md`](docs/safety_notes.md) | Notas de uso seguro en laboratorio. |
| [`docs/troubleshooting.md`](docs/troubleshooting.md) | Problemas comunes y soluciones. |
| [`docs/ros2_entrypoints_validation.md`](docs/ros2_entrypoints_validation.md) | Validación de comandos ROS 2. |
| [`docs/bom_template.csv`](docs/bom_template.csv) | Lista de materiales con costos y proveedores. |
| [`docs/license_overview.md`](docs/license_overview.md) | Estado de licencias y citación. |

## Firmware ESP32

El firmware final vive en [`firmware/`](firmware/).

```text
firmware/
├── ESP_IDF_BUILD_GUIDE.md
├── can_protocol/
├── esp32_joint_node/
│   ├── J1/
│   ├── J2/
│   ├── J3/
│   └── J4/
└── esp32_stepper_node/
    └── J5_tb6600/
```

Documentos clave: [`firmware/README.md`](firmware/README.md), [`firmware/ESP_IDF_BUILD_GUIDE.md`](firmware/ESP_IDF_BUILD_GUIDE.md), [`firmware/can_protocol/can_messages.md`](firmware/can_protocol/can_messages.md).

Compilar un nodo ESP32:

```bash
source /media/F15/Data/ESP_IDF_CONTAINER/v5.3.3/esp-idf/export.sh
cd ~/assistbelle-arm-elevator-subsystem/firmware/esp32_joint_node/J1
idf.py set-target esp32
idf.py build
```

## ROS 2

El software ROS 2 se mantiene dentro de [`ros2_ws/`](ros2_ws/).

```bash
cd ~/assistbelle-arm-elevator-subsystem/ros2_ws
source /opt/ros/jazzy/setup.bash
rm -rf build install log
colcon build --packages-select can_comm_pkg
source install/setup.bash
```

Crear CAN virtual:

```bash
sudo modprobe vcan
sudo ip link add dev can0 type vcan 2>/dev/null || true
sudo ip link set up can0
ros2 run can_comm_pkg can_node
```

Comandos principales a validar:

```bash
ros2 run can_comm_pkg control_teclado
ros2 run can_comm_pkg can_traj
ros2 run can_comm_pkg can_slider
ros2 run can_comm_pkg ik_node
ros2 run can_comm_pkg j5_ramp
ros2 run can_comm_pkg j5_trap
```

## Electrónica

La documentación electrónica se organiza en [`electronics/`](electronics/):

```text
electronics/
├── images/
├── pinout_tables/
├── power_distribution/
├── schematics/
└── wiring_diagrams/
```

Documentos principales:

- [`electronics/README.md`](electronics/README.md)
- [`electronics/schematics/README.md`](electronics/schematics/README.md)
- [`electronics/schematics/schematics_index.md`](electronics/schematics/schematics_index.md)
- [`electronics/pinout_tables/esp32_pinout_table.md`](electronics/pinout_tables/esp32_pinout_table.md)
- [`electronics/pinout_tables/raspberry_pi_mcp2515.md`](electronics/pinout_tables/raspberry_pi_mcp2515.md)
- [`electronics/wiring_diagrams/bus_principal.md`](electronics/wiring_diagrams/bus_principal.md)
- [`electronics/wiring_diagrams/nodos_controladores.md`](electronics/wiring_diagrams/nodos_controladores.md)
- [`electronics/power_distribution/power_summary.md`](electronics/power_distribution/power_summary.md)

Pendiente de cierre: verificar nombres finales de esquemáticos, mantener PDF/PNG junto al archivo editable, crear tabla de conectores, subir fotos reales y confirmar consistencia entre esquemático, pinout y firmware.

## Hardware mecánico

```text
hardware/
├── cad/
├── step/
├── stl/
├── drawings/
├── photos/
└── fasteners/
```

Falta subir CAD editable, exportar STEP/STL, completar fasteners/planos y agregar fotos mecánicas finales.

## Validación

La validación se organiza en [`validation/`](validation/):

```text
validation/
├── validation_plan.md
├── figures/
├── joint_motion_tests/
├── kinematics_tests/
├── media/
├── perception_tests/
└── pick_and_place_tests/
```

Falta copiar o enlazar videos finales, crear figuras, completar tablas de resultados, documentar CAN físico, pick-and-place y percepción.

## Lista de materiales

La BOM activa está en [`docs/bom_template.csv`](docs/bom_template.csv).

- 38 líneas activas de materiales/componentes.
- Componentes no usados removidos: Astra/Astra Plus, batería LiPo, tablet y DRV8825.
- Drivers finales diferenciados: DRV8871 para motores DC y TB6600 para NEMA.
- Costos registrados y referenciales agregados.
- Costo total preliminar activo: **S/ 4,328.63**.

## License

This repository uses a multi-license structure suitable for a HardwareX open-source hardware submission:

| Directory / asset type | License | License text |
|---|---|---|
| [`hardware/`](hardware/) | CERN-OHL-S v2.0 | [`LICENSES/CERN-OHL-S-2.0.txt`](LICENSES/CERN-OHL-S-2.0.txt) |
| [`electronics/`](electronics/) | CERN-OHL-S v2.0 | [`LICENSES/CERN-OHL-S-2.0.txt`](LICENSES/CERN-OHL-S-2.0.txt) |
| [`firmware/`](firmware/), [`ros2_ws/`](ros2_ws/), [`software/`](software/) | Apache-2.0 | [`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt) |
| Validation scripts and utilities | Apache-2.0 | [`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt) |
| [`docs/`](docs/), [`paper/`](paper/), images, figures, manuals and assembly instructions | CC-BY-4.0 | [`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt) |

The root [`LICENSE`](LICENSE) file summarizes the license policy. Detailed notes are in [`docs/license_overview.md`](docs/license_overview.md).

## Checklist de cierre

### Ya está avanzado

- [x] Estructura general del repositorio.
- [x] README principal reorganizado.
- [x] Documentación base en [`docs/`](docs/).
- [x] Firmware ESP32 migrado a [`firmware/`](firmware/).
- [x] Firmware J1-J5 compilado localmente.
- [x] ROS 2 compila localmente.
- [x] `can_node` inicia con `can0` virtual.
- [x] Pinouts ESP32 documentados.
- [x] Raspberry Pi + MCP2515 documentado.
- [x] Protocolo CAN documentado.
- [x] BOM inicial completada.
- [x] Plan de validación creado.
- [x] Multi-license policy creada.
- [x] `CITATION.cff` creado.
- [x] Estructura para esquemáticos creada en [`electronics/schematics/`](electronics/schematics/).

### Falta para una entrega HardwareX sólida

- [ ] Indexar y revisar nombres finales de esquemáticos.
- [ ] Probar todos los entry points ROS 2 principales.
- [ ] Validar CAN físico con ESP32 reales.
- [ ] Copiar o enlazar videos curados en [`validation/media/`](validation/media/).
- [ ] Completar tablas y figuras de validación.
- [ ] Completar tabla final de conectores.
- [ ] Subir fotos de electrónica.
- [ ] Subir CAD editable.
- [ ] Exportar STEP y STL.
- [ ] Completar fasteners y planos.
- [ ] Preparar figuras y tablas del manuscrito.
- [ ] Traducir documentación clave al inglés técnico.
- [ ] Revisar placeholders antes de publicación.

## Enfoque recomendado del artículo

Título tentativo:

**Open-source design and experimental validation of a CAN-based assistive robotic manipulator for medical supply handling**

El aporte principal del repositorio está en presentar un prototipo robótico reproducible con documentación completa de firmware, ROS 2, electrónica, comunicación CAN, BOM y validación experimental.

## Notas de publicación

- El sistema debe describirse como prototipo de laboratorio o entorno controlado.
- No afirmar desempeño clínico sin validación formal.
- No subir toolchains, builds ni archivos generados.
- Mantener los datos brutos separados de la validación curada.
- Usar [`docs/project_status.md`](docs/project_status.md) y [`docs/repository_audit.md`](docs/repository_audit.md) como fuente de verdad del avance.

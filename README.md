# Assistbelle / Robot asistivo 5-DOF

Repositorio de desarrollo y preparación para publicación tipo **HardwareX** de un manipulador robótico asistivo de 5 grados de libertad, orientado a tareas de laboratorio relacionadas con el traslado y manipulación de implementos médicos en un entorno controlado.

El sistema integra:

- **ROS 2** como capa principal de control, ejecución de nodos y teleoperación.
- **Bus CAN / SocketCAN** para comunicación entre el computador principal y los nodos de actuación.
- **ESP32 + ESP-IDF** para el firmware de articulaciones, elevador y gripper.
- **Drivers DRV8871** para motores DC.
- **Driver TB6600** para el eje prismático/elevador con motor NEMA.
- Documentación de electrónica, pinouts, firmware, validación, BOM y estructura de publicación.

La rama activa de preparación es:

```text
hardwarex-publication-package
```

## Autores

- Luciano Vergani
- Yuri Fabian Vilela Obando

## Propósito de esta rama

Esta rama organiza el repositorio para que el proyecto pueda convertirse en un paquete reproducible para HardwareX. El objetivo no es solo almacenar código, sino documentar de forma clara:

1. qué hardware se usó;
2. cómo se conecta;
3. cómo se compila el firmware;
4. cómo se ejecuta ROS 2;
5. cómo se validó el funcionamiento;
6. qué archivos faltan para cerrar la publicación.

## Estado actual

| Área | Estado | Evidencia / ubicación |
|---|---|---|
| Estructura del repositorio | Avanzada | `docs/repository_structure.md`, `docs/repository_audit.md` |
| Firmware ESP32 J1-J4 | Compila localmente | `firmware/esp32_joint_node/` |
| Firmware ESP32 J5/TB6600 | Compila localmente | `firmware/esp32_stepper_node/J5_tb6600/` |
| ROS 2 | Compila e inicia con `vcan` | `ros2_ws/`, `docs/ros2_entrypoints_validation.md` |
| CAN virtual | Validado | `can_node` inicia con `can0` virtual |
| Pinouts ESP32 | Documentados | `electronics/pinout_tables/esp32_pinout_table.md` |
| Raspberry Pi + MCP2515 | Documentado | `electronics/pinout_tables/raspberry_pi_mcp2515.md` |
| Protocolo CAN | Documentado | `firmware/can_protocol/can_messages.md` |
| BOM | Inicial completa | `docs/bom_template.csv` |
| Validación | Estructura lista | `validation/validation_plan.md`, `validation/media/media_index.md` |
| Licencia y citación | Inicial listo | `LICENSE`, `CITATION.cff` |
| CAD/STEP/STL | Pendiente crítico | `hardware/` |
| Diagramas eléctricos finales | Pendiente | `electronics/schematics/`, `electronics/wiring_diagrams/` |
| Paper | Pendiente | `paper/` |

## Estructura actual del repositorio

La estructura válida de esta rama es:

```text
robot-project/
├── README.md
├── LICENSE
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

### Carpetas principales

| Carpeta / archivo | Estado | Propósito |
|---|---|---|
| `README.md` | Activo | Entrada principal del repositorio. |
| `LICENSE` | Activo | Licencia principal actual: Apache-2.0. |
| `CITATION.cff` | Activo | Metadatos de citación del repositorio. |
| `requirements.txt` | Activo | Dependencias Python generales. |
| `docs/` | Activo | Estado, manuales, auditoría, checklist, BOM, seguridad y operación. |
| `electronics/` | Activo | Pinouts, cableado, potencia, esquemáticos e imágenes de electrónica. |
| `firmware/` | Activo | Firmware ESP32 organizado por nodo. |
| `hardware/` | Activo, pendiente de contenido final | CAD, STEP, STL, planos, fotos mecánicas y fasteners. |
| `paper/` | Activo, pendiente de manuscrito | Figuras, tablas, referencias y archivos del artículo. |
| `ros2_ws/` | Activo | Workspace ROS 2 completo del proyecto. |
| `software/` | Auxiliar | Guías de instalación y scripts que no sean nodos ROS 2. |
| `validation/` | Activo | Datos curados, tablas, figuras y evidencias de validación. |

### Carpetas temporales o legacy

| Carpeta | Estado recomendado | Acción |
|---|---|---|
| `Codigo_esp32/` | Temporal / legado local | No usar como carpeta final. Migrar solo código útil hacia `firmware/`. |
| `resultados/` | Bruto / histórico | Mantener como fuente de evidencias antiguas. Copiar solo resultados curados hacia `validation/`. |
| `.vscode/`, `.idea/`, `build/`, `install/`, `log/` | No versionar | Deben permanecer fuera del repositorio mediante `.gitignore`. |
| `hardware/CAD_editable/`, `hardware/STEP/`, `hardware/STL/` | Obsoleto si aparecen | Usar siempre `hardware/cad/`, `hardware/step/`, `hardware/stl/`. |

## Estructura HardwareX recomendada

La organización del paquete sigue esta lógica:

```text
hardwarex-package/
├── docs/                 # Manuales, checklist, BOM, auditoría, operación y seguridad
├── electronics/          # Pinouts, bus CAN, potencia, esquemáticos y fotos eléctricas
├── firmware/             # Firmware ESP32 reproducible con ESP-IDF
├── hardware/             # CAD, STEP, STL, planos y fotos mecánicas
├── ros2_ws/              # Software ROS 2 del robot
├── validation/           # Evidencias curadas, datos, figuras y videos
├── paper/                # Material del manuscrito
├── LICENSE
└── CITATION.cff
```

## Documentación principal

| Documento | Descripción |
|---|---|
| `docs/project_status.md` | Estado actual del proyecto y pendientes principales. |
| `docs/repository_audit.md` | Auditoría de avance y criterio de cierre. |
| `docs/repository_structure.md` | Reglas de organización de carpetas. |
| `docs/hardwarex_master_checklist.md` | Checklist maestro para cerrar la rama. |
| `docs/operation_manual.md` | Manual de operación con ROS 2, SocketCAN y ESP-IDF. |
| `docs/calibration_manual.md` | Guía inicial de calibración. |
| `docs/safety_notes.md` | Notas de uso seguro en laboratorio. |
| `docs/troubleshooting.md` | Errores conocidos y soluciones. |
| `docs/ros2_entrypoints_validation.md` | Validación de comandos ROS 2. |
| `docs/bom_template.csv` | Lista de materiales inicial con costos y proveedores. |
| `docs/license_overview.md` | Estado de licencias y citación. |

## Firmware ESP32

El firmware final vive en `firmware/`.

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

Estado:

- J1-J4: nodos de articulaciones rotativas con motores DC.
- J4: incluye control de gripper.
- J5: nodo de elevador con TB6600.
- El firmware J1-J5 fue compilado localmente.
- ESP-IDF no debe subirse al repositorio; se documenta como dependencia externa.

Compilar un nodo:

```bash
source /media/F15/Data/ESP_IDF_CONTAINER/v5.3.3/esp-idf/export.sh
cd ~/robot-project/firmware/esp32_joint_node/J1
idf.py set-target esp32
idf.py build
```

## ROS 2

El software ROS 2 se mantiene dentro de `ros2_ws/`.

Compilar:

```bash
cd ~/robot-project/ros2_ws
source /opt/ros/jazzy/setup.bash
rm -rf build install log
colcon build --packages-select can_comm_pkg
source install/setup.bash
```

Crear CAN virtual para pruebas sin hardware:

```bash
sudo modprobe vcan
sudo ip link add dev can0 type vcan 2>/dev/null || true
sudo ip link set up can0
```

Ejecutar nodo CAN:

```bash
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

La documentación electrónica se organiza en:

```text
electronics/
├── images/
├── pinout_tables/
├── power_distribution/
├── schematics/
└── wiring_diagrams/
```

Ya está documentado:

- pinout ESP32 por nodo;
- Raspberry Pi + MCP2515;
- bus principal 12 V, 5 V, GND, CANH y CANL;
- relación actuador-driver-nodo;
- protocolo CAN.

Falta completar:

- diagrama general final en imagen/PDF/KiCad;
- diagrama de potencia final;
- diagrama CAN final;
- fotos reales de electrónica;
- tabla final de conectores.

## Hardware mecánico

La estructura mecánica válida es:

```text
hardware/
├── cad/
│   ├── complete_robot/
│   ├── arm/
│   ├── elevator/
│   ├── gripper/
│   ├── mounts/
│   └── tooling/
├── step/
├── stl/
├── drawings/
├── photos/
└── fasteners/
```

Estado actual:

- La estructura de carpetas ya existe.
- Falta subir CAD editable.
- Falta exportar STEP.
- Falta exportar STL de piezas imprimibles.
- Falta tabla final de tornillos, tuercas, rodamientos y perfiles.
- Falta evidencia fotográfica mecánica final.

## Validación

La validación se organiza en:

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

Evidencias identificadas para curar:

| Evidencia bruta | Destino recomendado | Prueba |
|---|---|---|
| `resultados/Teclado_P1.mp4` | `validation/media/teleop_keyboard_test.mp4` | Teleoperación por teclado. |
| `resultados/j5_ramp_100.0mm_5reps.mp4` | `validation/media/j5_ramp_100mm_5reps.mp4` | Elevador J5 con perfil rampa. |
| `resultados/j5_trap_100.0mm_5reps.mp4` | `validation/media/j5_trapezoidal_100mm_5reps.mp4` | Elevador J5 con perfil trapezoidal. |

Falta:

- copiar o enlazar videos finales;
- crear figuras finales;
- completar tablas de resultados;
- documentar pruebas CAN físicas;
- documentar pruebas pick-and-place y percepción.

## Lista de materiales

La BOM inicial está en:

```text
docs/bom_template.csv
```

Estado:

- componentes principales organizados;
- costos registrados y referenciales agregados;
- componentes no usados removidos de la BOM activa;
- drivers finales diferenciados: DRV8871 para motores DC y TB6600 para NEMA.

La BOM sigue siendo preliminar hasta revisar precios finales, proveedores y cantidades exactas del diseño mecánico final.

## Checklist de cierre

### Ya está avanzado

- [x] Estructura general del repositorio.
- [x] README principal reorganizado.
- [x] Documentación base en `docs/`.
- [x] Firmware ESP32 migrado a `firmware/`.
- [x] Firmware J1-J5 compilado localmente.
- [x] ROS 2 compila localmente.
- [x] `can_node` inicia con `can0` virtual.
- [x] Pinouts ESP32 documentados.
- [x] Raspberry Pi + MCP2515 documentado.
- [x] Protocolo CAN documentado.
- [x] BOM inicial completada.
- [x] Plan de validación creado.
- [x] `LICENSE` creado.
- [x] `CITATION.cff` creado.

### Falta para una entrega HardwareX sólida

- [ ] Probar todos los entry points ROS 2 principales.
- [ ] Validar CAN físico con ESP32 reales.
- [ ] Copiar o enlazar videos curados en `validation/media/`.
- [ ] Completar tablas y figuras de validación.
- [ ] Completar diagramas eléctricos finales.
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
- Usar `docs/project_status.md` y `docs/repository_audit.md` como fuente de verdad del avance.

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Assistbelle robotic arm and elevator subsystem

Open-source HardwareX publication package for the **robotic arm and vertical elevator subsystem** of Assistbelle, intended for controlled laboratory experiments on the manipulation and transport of medical supplies.

This repository contains the hardware documentation, firmware, ROS 2 software, electronics documentation, validation material and publication support files needed to reproduce and evaluate the arm/elevator subsystem.

## Authors

- Yuri Fabian Vilela Obando
- Luciano Matteo Vergani Api

## Scope

This repository covers:

- robotic arm subsystem;
- vertical elevator / prismatic axis;
- ESP32 firmware for distributed joint control;
- CAN / SocketCAN communication;
- ROS 2 control and validation utilities;
- electronics documentation, pinouts, power distribution and schematics;
- bill of materials (BOM);
- validation documentation and curated evidence structure;
- documentation and paper-support material for HardwareX.

## Out of scope

The current public package does **not** cover:

- autonomous navigation;
- the complete mobile base;
- the storage module;
- real clinical validation or certified medical-device use.

The system must be interpreted as a **laboratory prototype** for controlled validation, not as a clinically approved device.

## Quick start

This flow verifies the ROS 2 package and the CAN bridge using a virtual CAN interface (`vcan`).

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

Expected output:

```text
CANNode iniciado y suscrito a /can_command
```

For ESP32 firmware, use [`firmware/ESP_IDF_BUILD_GUIDE.md`](firmware/ESP_IDF_BUILD_GUIDE.md).

## Repository structure

```text
assistbelle-arm-elevator-subsystem/
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

| Path | Purpose |
|---|---|
| [`docs/`](docs/) | General documentation, operation, safety, calibration, troubleshooting, BOM and checklists. |
| [`electronics/`](electronics/) | Schematics, wiring diagrams, power distribution, pinout tables and electronics images. |
| [`firmware/`](firmware/) | ESP32 firmware organized by joint/elevator node. |
| [`hardware/`](hardware/) | Mechanical CAD, STEP, STL, drawings, photos and fasteners. |
| [`paper/`](paper/) | Figures, tables, references and manuscript-support material. |
| [`ros2_ws/`](ros2_ws/) | ROS 2 workspace and `can_comm_pkg`. |
| [`software/`](software/) | Auxiliary software notes or scripts outside the ROS 2 workspace. |
| [`validation/`](validation/) | Curated validation data, media, figures and test summaries. |

Legacy folders from the development repository, such as `Codigo_esp32/` or `resultados/`, are not part of the recommended public structure. Useful firmware should be kept under [`firmware/`](firmware/), and curated evidence should be kept under [`validation/`](validation/).

## Documentation map

| Document | Description |
|---|---|
| [`docs/README.md`](docs/README.md) | Documentation index. |
| [`docs/project_status.md`](docs/project_status.md) | Current project status and immediate pending items. |
| [`docs/repository_audit.md`](docs/repository_audit.md) | Repository audit and closure criteria. |
| [`docs/repository_structure.md`](docs/repository_structure.md) | Repository organization rules. |
| [`docs/hardwarex_master_checklist.md`](docs/hardwarex_master_checklist.md) | Master checklist for HardwareX completion. |
| [`docs/publication_checklist.md`](docs/publication_checklist.md) | Publication-oriented checklist. |
| [`docs/operation_manual.md`](docs/operation_manual.md) | Operation steps for ROS 2, SocketCAN and ESP-IDF. |
| [`docs/calibration_manual.md`](docs/calibration_manual.md) | Initial calibration procedure. |
| [`docs/safety_notes.md`](docs/safety_notes.md) | Safety notes for laboratory operation. |
| [`docs/troubleshooting.md`](docs/troubleshooting.md) | Common errors and fixes. |
| [`docs/ros2_entrypoints_validation.md`](docs/ros2_entrypoints_validation.md) | ROS 2 command validation routine. |
| [`docs/bom_template.csv`](docs/bom_template.csv) | Active bill of materials. |
| [`docs/license_overview.md`](docs/license_overview.md) | Multi-license policy. |

## Current status

| Area | Status | Reference |
|---|---|---|
| Repository organization | Advanced | [`docs/repository_structure.md`](docs/repository_structure.md) |
| ESP32 firmware J1-J4 | Locally compiled | [`firmware/esp32_joint_node/`](firmware/esp32_joint_node/) |
| ESP32 firmware J5 / TB6600 | Locally compiled | [`firmware/esp32_stepper_node/J5_tb6600/`](firmware/esp32_stepper_node/J5_tb6600/) |
| ROS 2 / CAN bridge | Builds and starts with `vcan` | [`ros2_ws/`](ros2_ws/), [`docs/ros2_entrypoints_validation.md`](docs/ros2_entrypoints_validation.md) |
| ESP32 pinouts | Documented | [`electronics/pinout_tables/esp32_pinout_table.md`](electronics/pinout_tables/esp32_pinout_table.md) |
| Raspberry Pi + MCP2515 | Documented | [`electronics/pinout_tables/raspberry_pi_mcp2515.md`](electronics/pinout_tables/raspberry_pi_mcp2515.md) |
| CAN protocol | Documented | [`firmware/can_protocol/can_messages.md`](firmware/can_protocol/can_messages.md) |
| BOM | Preliminary complete | [`docs/bom_template.csv`](docs/bom_template.csv) |
| Schematics | In progress | [`electronics/schematics/`](electronics/schematics/) |
| Validation | Structure ready | [`validation/validation_plan.md`](validation/validation_plan.md) |
| Mechanical CAD / STEP / STL | Pending | [`hardware/`](hardware/) |
| Paper material | Pending | [`paper/`](paper/) |

## Firmware ESP32

The final ESP32 firmware is kept in [`firmware/`](firmware/):

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

Example build command:

```bash
source /path/to/esp-idf/export.sh
cd firmware/esp32_joint_node/J1
idf.py set-target esp32
idf.py build
```

## ROS 2

The ROS 2 workspace is kept in [`ros2_ws/`](ros2_ws/):

```bash
cd ros2_ws
source /opt/ros/jazzy/setup.bash
rm -rf build install log
colcon build --packages-select can_comm_pkg
source install/setup.bash
```

Main commands to validate:

```bash
ros2 run can_comm_pkg can_node
ros2 run can_comm_pkg control_teclado
ros2 run can_comm_pkg can_traj
ros2 run can_comm_pkg can_slider
ros2 run can_comm_pkg ik_node
ros2 run can_comm_pkg j5_ramp
ros2 run can_comm_pkg j5_trap
```

## Electronics

Electronics documentation is organized in [`electronics/`](electronics/):

```text
electronics/
├── images/
├── pinout_tables/
├── power_distribution/
├── schematics/
└── wiring_diagrams/
```

Current documentation includes ESP32 pinouts, Raspberry Pi + MCP2515 wiring, CAN/power bus notes, power-distribution notes and a schematics index. Final schematic exports, electronics photos and connector tables remain pending.

## Mechanical hardware

Mechanical design files should be organized as:

```text
hardware/
├── cad/
├── step/
├── stl/
├── drawings/
├── photos/
└── fasteners/
```

Editable CAD, STEP/STL exports, drawings, fasteners and final mechanical photos remain pending.

## Validation

Validation material is organized in [`validation/`](validation/):

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

Pending work includes curated videos, final CSV files, figures, physical CAN validation, pick-and-place validation and perception validation.

## Bill of materials

The active BOM is available at [`docs/bom_template.csv`](docs/bom_template.csv).

Current notes:

- 38 active material/component lines.
- Unused components removed from the active BOM: Astra/Astra Plus, LiPo battery, tablet and DRV8825.
- DRV8871 and TB6600 are differentiated in the active design documentation.
- Preliminary total: **S/ 4,328.63**.

## License

This repository uses a multi-license structure suitable for a HardwareX open-source hardware submission:

| Directory / asset type | License | License text |
|---|---|---|
| [`hardware/`](hardware/) | CERN-OHL-S v2.0 | [`LICENSES/CERN-OHL-S-2.0.txt`](LICENSES/CERN-OHL-S-2.0.txt) |
| [`electronics/`](electronics/) | CERN-OHL-S v2.0 | [`LICENSES/CERN-OHL-S-2.0.txt`](LICENSES/CERN-OHL-S-2.0.txt) |
| [`firmware/`](firmware/), [`ros2_ws/`](ros2_ws/), [`software/`](software/) | Apache-2.0 | [`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt) |
| Validation scripts and utilities | Apache-2.0 | [`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt) |
| [`docs/`](docs/), [`paper/`](paper/), images, figures, manuals and assembly instructions | CC-BY-4.0 | [`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt) |

The root [`LICENSE`](LICENSE) file summarizes this policy. See [`docs/license_overview.md`](docs/license_overview.md) for details.

## Remaining HardwareX closure items

- [ ] Confirm final schematic filenames and exports.
- [ ] Update [`electronics/power_distribution/power_summary.md`](electronics/power_distribution/power_summary.md).
- [ ] Create a final connector table.
- [ ] Add electronics photos.
- [ ] Validate all ROS 2 entry points from a clean clone.
- [ ] Validate physical CAN with ESP32 nodes.
- [ ] Add CAD, STEP and STL files.
- [ ] Curate validation videos, CSV files and final figures.
- [ ] Prepare paper figures, tables and references.
- [ ] Translate final documentation to technical English where needed.

## Recommended article focus

**Open-source design and experimental validation of a CAN-based assistive robotic manipulator for medical supply handling**

The main contribution is a reproducible robotic arm/elevator subsystem with firmware, ROS 2 control, CAN communication, electronics documentation, BOM and experimental validation material for controlled laboratory use.

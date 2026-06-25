<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# HardwareX manuscript outline

Working outline for a HardwareX-style manuscript describing the Assistbelle arm and elevator subsystem.

This outline focuses on the open-source hardware package currently represented in the repository. The present repository state is strongest for the vertical elevator subsystem, distributed CAN-based control architecture, BOM, CAD package and supporting firmware/ROS 2 structure.

## Proposed title

**Open-source arm and vertical elevator subsystem for a low-cost assistive healthcare robot**

Alternative shorter title:

**Assistbelle: an open-source robotic arm and vertical elevator subsystem for assistive healthcare robotics**

## Article structure

### 1. Hardware in context

Purpose:

- describe the healthcare-assistive motivation;
- position the subsystem as part of a larger assistive mobile robot;
- clarify that the repository focuses on the arm/elevator subsystem and its electronics/control stack;
- define current scope as laboratory prototype / controlled environment, not clinical deployment.

Key points to include:

- low-cost assistive robotics;
- vertical positioning of the manipulator through a screw-driven elevator;
- modular distributed electronics with ESP32 nodes and CAN communication;
- Raspberry Pi 5 running ROS 2 as the high-level controller.

### 2. Hardware description

Purpose:

- explain the mechanical, electronic and software architecture;
- describe how the elevator, arm control nodes and CAN bus interact.

Suggested subsections:

#### 2.1 System overview

- Assistbelle subsystem boundaries.
- Vertical elevator + robotic arm + gripper/control support.
- Out-of-scope elements: complete mobile base, clinical deployment, autonomous navigation package if not included in this repository.

#### 2.2 Mechanical design

- V-slot frame and fabricated plates.
- Dual NEMA 23 + TR8 lead screw elevator concept.
- Dual V-wheel guiding system.
- Fabricated/printed custom components.
- Current CAD snapshot: v60 working snapshot.

Important repository references:

- `hardware/cad/complete_robot/ASM_Elevator_System_v60.f3z`
- `hardware/step/ASM_Elevator_System_v60.step`
- `hardware/design_files_index.md`
- `paper/tables/design_files_summary.md`

#### 2.3 Electronics and power architecture

- Dell server PSU actuator supply, exact model pending.
- LM2596S 5 V logic rail.
- Panic/emergency button design intent: actuator power interrupted, logic remains powered.
- Raspberry Pi 5 + MCP2515 CAN interface.
- ESP32 distributed nodes with CAN transceivers.
- Driver assignment:
  - J1/J4: DRV8871;
  - J2/J3: IBT-2/BTS7960;
  - J5: two TB6600 stepper drivers.

Important repository references:

- `electronics/wiring_diagrams/connector_table.md`
- `electronics/wiring_diagrams/bus_principal.md`
- `electronics/power_distribution/power_summary.md`
- `electronics/pinout_tables/esp32_pinout_table.md`
- `electronics/pinout_tables/raspberry_pi_mcp2515.md`

#### 2.4 Firmware and communication protocol

- ESP-IDF firmware structure for J1-J5.
- CAN IDs A/B/C/D.
- J5 command format: `C5` as `float32` target position in mm.
- J5 compatibility note: `B5` final payload decision pending physical validation.

Important repository references:

- `firmware/esp32_joint_node/`
- `firmware/esp32_stepper_node/J5_tb6600/`
- `firmware/can_protocol/can_messages.md`

#### 2.5 ROS 2 software

- `can_comm_pkg` package.
- SocketCAN `can_node`.
- `/can_command`, `/motors_state`, `/joint_states`.
- Validation entry points for J1-J5, including `j5_step`, `j5_ramp`, `j5_trap`.

Important repository references:

- `ros2_ws/src/can_comm_pkg/`
- `docs/ros2_entrypoints_validation.md`

### 3. Design files

Purpose:

- summarize available editable, neutral and fabrication files.
- explain v60 as working snapshot, not final frozen release.

Use:

- `paper/tables/design_files_summary.md`

Suggested text:

> The design package includes an editable Fusion 360 archive, a neutral STEP assembly, STL files for custom fabricated/printed components, PDF drawings for fabricated plates and DXF files for laser/waterjet cutting. The currently uploaded CAD package is marked as v60 and should be treated as a working snapshot until a final release tag is frozen.

### 4. Bill of materials

Purpose:

- describe the cost and component categories.
- reference the machine-readable BOM.

Use:

- `docs/bom/hardwarex_elevator_bom_final.csv`
- `docs/bom/hardwarex_elevator_bom_final.md`
- `paper/tables/bom_summary.md`

Key values:

| Metric | Value |
|---|---:|
| BOM items | 32 |
| Estimated product/material total | USD 484.78 |
| Structure subtotal | USD 122.14 |
| Actuation subtotal | USD 81.58 |
| Guiding subtotal | USD 78.30 |
| Fasteners subtotal | USD 37.51 |
| Electronics subtotal | USD 165.25 |

### 5. Build instructions

Current status:

- mechanical design files are available;
- detailed step-by-step physical assembly instructions still need to be written;
- photos are deferred until robot access.

Suggested content:

1. Fabricate base/top/gantry plates from drawings and DXF files.
2. Prepare V-slot frame and brackets according to the CAD assembly.
3. Install V-wheel guide assemblies and spacer blocks.
4. Install NEMA 23 motors, couplers, TR8 lead screws and nut blocks.
5. Install electronics and wiring harness.
6. Verify 5 V logic rail before connecting Raspberry Pi/ESP32 nodes.
7. Verify CAN wiring and termination.
8. Run firmware/ROS 2 tests.

### 6. Operation instructions

Include:

- powering sequence;
- emergency/panic button behavior;
- ROS 2 startup with SocketCAN;
- J5 movement commands;
- expected state topics.

Repository references:

- `docs/operation_manual.md`
- `docs/troubleshooting.md`
- `docs/safety_notes.md`
- `docs/ros2_entrypoints_validation.md`

### 7. Validation and characterization

Current status:

- validation folder structure exists;
- initial J5 validation references exist;
- final physical CAN validation, curated CSVs, videos and figures remain pending.

Suggested subsections:

- J5 elevator motion tests.
- ROS 2 / SocketCAN validation.
- CAN payload compatibility status.
- Mechanical/electrical physical verification pending items.

Repository references:

- `validation/`
- `docs/ros2_entrypoints_validation.md`
- `firmware/can_protocol/can_messages.md`

### 8. Safety

Include:

- laboratory prototype only;
- not certified for clinical use;
- actuator power separated from logic power by design intent;
- panic button cuts actuator power while leaving Raspberry Pi/ESP32/CAN powered;
- mechanical self-locking note for J2/J3 if included in final arm description;
- verify 5 V before connecting logic loads;
- verify CANH/CANL orientation before powering.

Repository references:

- `docs/safety_notes.md`
- `electronics/power_distribution/power_summary.md`
- `electronics/wiring_diagrams/bus_principal.md`

### 9. Data availability

Use:

- `paper/data_availability_statement.md`

Core message:

- repository is public;
- v60 CAD is available as a working snapshot;
- design files, BOM, firmware and ROS 2 package are included;
- photos and final physical wiring evidence are deferred until robot access;
- final submission should use a frozen GitHub release/tag.

### 10. References

To be completed with literature and documentation references used in the thesis/manuscript.

Likely reference groups:

- assistive robots in healthcare;
- open-source hardware / HardwareX methodology;
- CAN bus / distributed motor control references if needed;
- ROS 2 and ESP32/TWAI documentation if cited;
- mechanical components / V-slot / lead screw references if appropriate.

## Figures still needed

| Figure | Status | Source idea |
|---|---|---|
| System architecture diagram | Pending | Draw from Raspberry Pi, CAN bus, ESP32 nodes and drivers. |
| Mechanical CAD render | Pending | Export from Fusion 360 v60. |
| Elevator assembly figure | Pending | Use CAD screenshot until physical photos are available. |
| Electronics block diagram | Pending | Derive from `bus_principal.md` and `connector_table.md`. |
| CAN protocol diagram | Pending | Derive from `can_messages.md`. |
| Validation plots | Pending | Generate from curated CSVs. |

## Tables already prepared

| Table | File | Status |
|---|---|---|
| Design files summary | `paper/tables/design_files_summary.md` | Ready as Markdown draft. |
| BOM summary | `paper/tables/bom_summary.md` | Ready as Markdown draft. |

## Open decisions before final manuscript

- Freeze final CAD/BOM version and tag a GitHub release.
- Confirm TB6600 supply voltage physically.
- Confirm exact Dell PSU model.
- Confirm physical CAN termination locations.
- Decide final `B5` payload behavior for J5.
- Add prototype photos once available.
- Curate validation data, videos and figures.
- Replace Raspberry Pi 5 cost estimate with exact selected supplier/product.

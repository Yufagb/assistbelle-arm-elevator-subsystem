<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Design files summary table

This table summarizes the main design files currently available for the Assistbelle elevator subsystem HardwareX package.

The current uploaded CAD package is **v60**, treated as a working snapshot rather than a final frozen release. Physical prototype photos are deferred until the robot is available again.

## Mechanical design files

| File | Format | Location | Purpose | Editable? | Status |
|---|---|---|---|---|---|
| `ASM_Elevator_System_v60.f3z` | Fusion 360 archive | `hardware/cad/complete_robot/` | Complete editable CAD assembly for the current elevator snapshot. | Yes | Uploaded via Git LFS. |
| `ASM_Elevator_System_v60.step` | STEP | `hardware/step/` | Neutral CAD export for users without Fusion 360. | No | Uploaded via Git LFS. |
| `FAB_ACT_002_NEMA23_Mounting_Plate_ABS_v60.stl` | STL | `hardware/stl/` | Printable/fabricated NEMA 23 mounting plate. | No | Uploaded via Git LFS. |
| `FAB_GUI_002_Spacer_Block_ABS_Gray_v60.stl` | STL | `hardware/stl/` | Printable/fabricated spacer block for the V-wheel guide assembly. | No | Uploaded via Git LFS. |
| `FAB_STR_001_Base_Plate_356x356x15_MDF_v60.pdf` | PDF drawing | `hardware/drawings/` | Fabrication drawing for the MDF base plate. | No | Uploaded. |
| `FAB_STR_002_Top_Plate_420x400x3_StainlessSteel_v60.pdf` | PDF drawing | `hardware/drawings/` | Fabrication drawing for the stainless-steel top plate. | No | Uploaded. |
| `FAB_GUI_001_Gantry_Plate_127x88x3_StainlessSteel_v60.pdf` | PDF drawing | `hardware/drawings/` | Fabrication drawing for the stainless-steel gantry plate. | No | Uploaded. |
| `FAB_STR_002_Top_Plate_420x400x3_StainlessSteel_v60.dxf` | DXF | `hardware/drawings/` | Laser/waterjet cutting geometry for the top plate. | No | Uploaded via Git LFS. |
| `FAB_GUI_001_Gantry_Plate_127x88x3_StainlessSteel_v60.dxf` | DXF | `hardware/drawings/` | Laser/waterjet cutting geometry for the gantry plate. | No | Uploaded via Git LFS. |

## Electronics and firmware design files

| File / folder | Format | Location | Purpose | Status |
|---|---|---|---|---|
| `schematics_index.md` | Markdown | `electronics/schematics/` | Index of reviewed schematic PDF exports. | Available. |
| `connector_table.md` | Markdown | `electronics/wiring_diagrams/` | Connector inventory from schematics, documentation and confirmed design intent. | Working table; physical pin order/wire colors pending. |
| `bus_principal.md` | Markdown | `electronics/wiring_diagrams/` | Main 12 V / 5 V / CAN bus description and termination notes. | Updated with confirmed design intent. |
| `power_summary.md` | Markdown | `electronics/power_distribution/` | Power architecture, panic-button behavior and pending electrical checks. | Updated with confirmed design intent. |
| `esp32_pinout_table.md` | Markdown | `electronics/pinout_tables/` | ESP32 pin table derived from firmware. | Available. |
| `raspberry_pi_mcp2515.md` | Markdown | `electronics/pinout_tables/` | Raspberry Pi 5 to MCP2515 wiring and setup notes. | Available. |
| `can_messages.md` | Markdown | `firmware/can_protocol/` | CAN IDs, payloads and J5 ROS/firmware compatibility status. | Updated; final B5 decision pending. |
| `ESP_IDF_BUILD_GUIDE.md` | Markdown | `firmware/` | ESP-IDF build guide for firmware projects. | Available. |
| `esp32_joint_node/` | ESP-IDF C firmware | `firmware/` | J1-J4 ESP32 firmware projects. | Included. |
| `esp32_stepper_node/J5_tb6600/` | ESP-IDF C firmware | `firmware/` | J5/elevator TB6600 firmware project. | Included; B5 payload closeout pending validation. |
| `can_comm_pkg` | ROS 2 Python package | `ros2_ws/src/` | SocketCAN bridge, trajectory tools, control apps and validation entry points. | Included; clean-clone entry-point validation pending. |

## Deferred files

| File type | Reason for deferral | Planned location |
|---|---|---|
| Mechanical photos | Physical robot is not currently available for imaging. | `hardware/photos/` |
| Electronics photos | Physical robot/electronics are not currently available for imaging. | `electronics/images/` |
| Subsystem STEP exports | Optional for current v60 working snapshot; may be added before final release freeze. | `hardware/step/` |
| Final physical connector evidence | Requires inspection/photos of the robot. | `electronics/wiring_diagrams/` and `electronics/images/` |

## Notes for manuscript use

- Use the complete Fusion 360 archive and STEP assembly as the primary design-file references.
- Use STL files only for custom printed/fabricated parts, not for purchased components.
- Use DXF files for cutting stainless-steel plates.
- Mention that v60 is a working snapshot and that a final frozen release should be tagged before submission.

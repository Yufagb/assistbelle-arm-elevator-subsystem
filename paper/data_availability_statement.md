<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Data availability statement

All public design files, bill of materials, firmware, ROS 2 software, validation structure and documentation for the Assistbelle arm and elevator subsystem are maintained in the GitHub repository:

```text
https://github.com/Yufagb/assistbelle-arm-elevator-subsystem
```

The repository is organized to support reproducibility of the vertical elevator subsystem and the associated distributed control architecture used in the laboratory prototype.

## Publicly available materials

| Material type | Repository location | Availability status |
|---|---|---|
| Editable CAD assembly | `hardware/cad/complete_robot/ASM_Elevator_System_v60.f3z` | Available as the current v60 working snapshot through Git LFS. |
| Neutral CAD assembly | `hardware/step/ASM_Elevator_System_v60.step` | Available as the current v60 working snapshot through Git LFS. |
| Printable/fabricated part files | `hardware/stl/` | Available for the NEMA 23 mounting plate and spacer block. |
| Fabrication drawings | `hardware/drawings/*.pdf` | Available for the MDF base plate, stainless-steel top plate and stainless-steel gantry plate. |
| Cutting files | `hardware/drawings/*.dxf` | Available for the stainless-steel top plate and gantry plate. |
| Bill of materials | `docs/bom/hardwarex_elevator_bom_final.csv` | Available as machine-readable CSV. |
| BOM summary | `docs/bom/hardwarex_elevator_bom_final.md`, `paper/tables/bom_summary.md` | Available as GitHub-readable Markdown. |
| Electronics documentation | `electronics/` | Available as schematics index, wiring tables, pinouts and power/CAN summaries. |
| Firmware | `firmware/` | Available as ESP-IDF projects for J1-J5 and CAN protocol documentation. |
| ROS 2 software | `ros2_ws/src/can_comm_pkg/` | Available as a ROS 2 Python package with SocketCAN interface and control/validation entry points. |
| Validation structure | `validation/` | Available as folder structure and preliminary J5 validation references. |

## Materials deferred until physical access

The following evidence is intentionally marked as deferred because the physical prototype is not currently available for imaging or measurement:

| Deferred material | Planned repository location | Reason |
|---|---|---|
| Mechanical prototype photos | `hardware/photos/` | Requires physical access to the assembled robot. |
| Electronics photos | `electronics/images/` | Requires physical access to wiring, drivers and power hardware. |
| Final connector pin order, wire colors and cable gauges | `electronics/wiring_diagrams/connector_table.md` | Requires physical inspection. |
| TB6600 supply voltage confirmation | `electronics/power_distribution/power_summary.md` | Requires measurement or inspection on the robot. |
| CAN termination physical locations | `electronics/wiring_diagrams/bus_principal.md` | Requires physical inspection. |
| Physical CAN validation logs | `validation/` | Requires robot/electronics test session. |

## Current versioning status

The current CAD files are stored as **v60 working snapshots**. They are suitable for repository progress tracking and review, but the final HardwareX submission should use a frozen release tag or clearly declared final CAD/BOM version.

Recommended final-release actions:

1. Freeze the final CAD version.
2. Re-export the full `.f3z` and `.step` files.
3. Re-export any changed STL, PDF or DXF fabrication files.
4. Re-check BOM quantities and costs against the frozen CAD.
5. Tag the GitHub release used by the manuscript.

## Reuse and licensing

The repository uses a multi-license structure:

- hardware design files: CERN-OHL-S-2.0;
- software, firmware and scripts: Apache-2.0;
- documentation, tables and manuscript materials: CC-BY-4.0.

Users should follow the license statements in the root `LICENSE`, `LICENSES/` folder and `docs/license_overview.md`.

## Suggested manuscript wording

A concise statement suitable for the HardwareX manuscript is:

> The design files, bill of materials, firmware, ROS 2 software, validation structure and documentation associated with this hardware are available in the public GitHub repository `Yufagb/assistbelle-arm-elevator-subsystem`. The current repository includes the v60 working CAD snapshot, neutral STEP export, STL and DXF fabrication files, PDF drawings, electronics documentation, ESP32 firmware and ROS 2 communication package. Prototype photographs and final physical wiring evidence are marked as deferred and will be added once physical access to the robot is available. The repository uses CERN-OHL-S-2.0 for hardware design files, Apache-2.0 for software/firmware and CC-BY-4.0 for documentation and manuscript materials.

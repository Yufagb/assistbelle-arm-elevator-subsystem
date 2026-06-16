<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Electrical schematics

This folder contains the electrical schematic PDFs for the Assistbelle robotic arm and elevator subsystem.

The schematics document the main power/CAN bus, Raspberry Pi to MCP2515 interface, ESP32-based DC motor controller nodes, IBT-2-based DC motor controller nodes and the J5 stepper/elevator controller.

## Available schematic PDFs

| File | Subsystem | Main content | HardwareX status |
|---|---|---|---|
| `Main Bus.pdf` | Main power and CAN bus | 12V, P_GND, 5V, S_GND, CANH, CANL, subsystem branches and RT1/RT2 120-ohm CAN terminations. | Reviewed; physical implementation still pending. |
| `RASPBERRYPI_MCP2515.pdf` | Raspberry Pi to MCP2515 interface | Raspberry Pi 40-pin header, MCP2515 10-pin header, SPI, interrupt, CAN connector and 5V power connector. | Reviewed; final implementation uses 5 V module power and must preserve Raspberry Pi 3.3 V logic compatibility. |
| `DC_MOTOR_DRIVER_SCH.pdf` | DRV8871 DC motor controller | ESP32 NodeMCU, SN65HVD230DR, DRV8871DDA, CAN header, power headers and motor/encoder header. | Reviewed; intended for J1/J4 documentation, physical assignment pending. |
| `DC_MOTOR_DRIVER_SCH_IBT2.pdf` | IBT-2 DC motor controller | ESP32 NodeMCU, SN65HVD230DR, IBT-2 interface, CAN header, power headers and motor/encoder header. | Reviewed; intended for J2/J3 documentation, physical assignment pending. |
| `Stepper Driver v7.pdf` | J5 stepper/elevator controller | ESP32 NodeMCU, CAN transceiver, J_CAN, J_DRIVERS with ENA/DIR/PUL and J_5V. | Reviewed; physical assignment pending. |

## Extracted design coverage

| Requirement | Covered by | Notes |
|---|---|---|
| 12 V actuator rail | `Main Bus.pdf`, motor-driver schematics | Main Bus separates 12V and P_GND. |
| 5 V logic rail | `Main Bus.pdf`, `RASPBERRYPI_MCP2515.pdf`, motor-driver schematics, `Stepper Driver v7.pdf` | Final implementation uses 5 V for the MCP2515 module and 5 V logic distribution from the LM2596S rail. |
| Separate power/signal grounds | `Main Bus.pdf` | Main Bus labels P_GND and S_GND separately. |
| CANH/CANL bus | All five schematics | CAN connector or SN65HVD230DR shown in controller sheets. |
| CAN termination | `Main Bus.pdf` | RT1 and RT2 are shown as 120-ohm terminations. |
| Raspberry Pi + MCP2515 | `RASPBERRYPI_MCP2515.pdf` | Includes SPI, INT_CAN, 5 V power connector and CAN connector. |
| DRV8871 DC motor node | `DC_MOTOR_DRIVER_SCH.pdf` | Includes DRV8871DDA and ILIM path. |
| IBT-2 DC motor node | `DC_MOTOR_DRIVER_SCH_IBT2.pdf` | Includes IBT2_CONN, IBT_POWER_HEADER and IBT_MOTOR_HEADER. |
| J5 stepper/elevator node | `Stepper Driver v7.pdf` | Includes PUL, DIR and ENA signals. |

## Files derived from this schematic review

The following repository documents use information extracted from these PDFs:

- [`schematics_index.md`](schematics_index.md): indexed schematic summary and extracted connector/component information.
- [`../wiring_diagrams/connector_table.md`](../wiring_diagrams/connector_table.md): connector table extracted from the schematic PDFs.
- [`../wiring_diagrams/nodos_controladores.md`](../wiring_diagrams/nodos_controladores.md): node-to-driver assignment and physical verification checklist.
- [`../power_distribution/power_summary.md`](../power_distribution/power_summary.md): power architecture summary.

## Physical verification still required

Before final HardwareX submission, verify on the real robot:

- [ ] the exact location of RT1 and RT2 CAN termination resistors;
- [ ] the MCP2515 module is powered from 5 V and safely interfaces with Raspberry Pi 3.3 V SPI/INT logic;
- [ ] the physical driver assignment: J1 DRV8871, J2 IBT-2, J3 IBT-2, J4 DRV8871 + servo, J5 TB6600;
- [ ] connector models, pin order, wire colors and cable gauges;
- [ ] the actual panic-button wiring path for actuator power cut-off;
- [ ] final photos for [`../images/`](../images/).

## Export and naming recommendations

For final publication, keep the current PDFs and optionally export PNG previews with these names:

| Optional PNG export | Source PDF |
|---|---|
| `schematic_main_bus.png` | `Main Bus.pdf` |
| `schematic_raspberrypi_mcp2515.png` | `RASPBERRYPI_MCP2515.pdf` |
| `schematic_drv8871_node.png` | `DC_MOTOR_DRIVER_SCH.pdf` |
| `schematic_ibt2_node.png` | `DC_MOTOR_DRIVER_SCH_IBT2.pdf` |
| `schematic_stepper_j5_node.png` | `Stepper Driver v7.pdf` |

If editable KiCad or EDA source files exist, keep them together with the PDF/PNG exports in this folder.

## Related documents

- [`../README.md`](../README.md)
- [`schematics_index.md`](schematics_index.md)
- [`../pinout_tables/esp32_pinout_table.md`](../pinout_tables/esp32_pinout_table.md)
- [`../pinout_tables/raspberry_pi_mcp2515.md`](../pinout_tables/raspberry_pi_mcp2515.md)
- [`../wiring_diagrams/bus_principal.md`](../wiring_diagrams/bus_principal.md)
- [`../wiring_diagrams/nodos_controladores.md`](../wiring_diagrams/nodos_controladores.md)
- [`../wiring_diagrams/connector_table.md`](../wiring_diagrams/connector_table.md)
- [`../power_distribution/power_summary.md`](../power_distribution/power_summary.md)

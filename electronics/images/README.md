<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Electronics images

This folder stores the final electronics photos and schematic captures used to document the Assistbelle robotic arm and elevator subsystem for HardwareX.

## Purpose

The photos in this folder should make the electronics reproducible by showing the real implementation, connector orientation, driver assignment and wiring layout.

## Required photo set

| Image filename | Content to capture | Required evidence | Status |
|---|---|---|---|
| `electronics_overview.jpg` | General electronics layout. | Full view of power supply, logic electronics, drivers and wiring. | Pending |
| `dell_server_psu_label.jpg` | Dell server power-supply label. | Exact model, 12 V rating and current rating. | Pending |
| `lm2596s_converter.jpg` | DC-DC LM2596S module. | Input wiring, output wiring and module location. | Pending |
| `panic_button_wiring.jpg` | Panic-button or emergency cut-off wiring. | Evidence that actuator power is interrupted while logic remains powered. | Pending |
| `main_bus_wiring.jpg` | Main bus wiring. | 12V, P_GND, 5V, S_GND, CANH and CANL routing. | Pending |
| `can_termination_rt1.jpg` | CAN termination RT1. | 120-ohm resistor location at one end of CAN bus. | Pending |
| `can_termination_rt2.jpg` | CAN termination RT2. | 120-ohm resistor location at the other end of CAN bus. | Pending |
| `raspberry_pi_mcp2515.jpg` | Raspberry Pi 5 to MCP2515 wiring. | SPI, INT, power and CAN connection. | Pending |
| `j1_drv8871_node.jpg` | J1 controller node. | ESP32, DRV8871, encoder/motor/power/CAN connectors. | Pending |
| `j2_ibt2_node.jpg` | J2 controller node. | ESP32, IBT-2, encoder/motor/power/CAN connectors. | Pending |
| `j3_ibt2_node.jpg` | J3 controller node. | ESP32, IBT-2, encoder/motor/power/CAN connectors. | Pending |
| `j4_drv8871_gripper_node.jpg` | J4 controller node and gripper connection. | ESP32, DRV8871, servo/gripper wiring and connectors. | Pending |
| `j5_tb6600_node.jpg` | J5 elevator controller node. | ESP32, TB6600, PUL/DIR/ENA, power and CAN connectors. | Pending |

## Optional schematic captures

If PDF schematics are not easy to view in the final paper package, export or capture the following images:

| Image filename | Source schematic |
|---|---|
| `schematic_main_bus.png` | `electronics/schematics/Main Bus.pdf` |
| `schematic_raspberrypi_mcp2515.png` | `electronics/schematics/RASPBERRYPI_MCP2515.pdf` |
| `schematic_drv8871_node.png` | `electronics/schematics/DC_MOTOR_DRIVER_SCH.pdf` |
| `schematic_ibt2_node.png` | `electronics/schematics/DC_MOTOR_DRIVER_SCH_IBT2.pdf` |
| `schematic_stepper_j5_node.png` | `electronics/schematics/Stepper Driver v7.pdf` |

## Photo checklist

Before final HardwareX submission, each photo should have:

- clear focus;
- sufficient lighting;
- visible connector orientation;
- visible labels or annotations when needed;
- no personal or unrelated background information;
- consistent filename using lowercase words and underscores;
- corresponding reference from `electronics/wiring_diagrams/connector_table.md` when applicable.

## Information to record with each photo

For each photo, record the following in the commit message, file name or related documentation:

| Field | Example |
|---|---|
| Subsystem | J2 IBT-2 controller node |
| Related connector IDs | `C-IBT2-CTRL`, `C-IBT2-CAN`, `C-IBT2-PWR` |
| Signals visible | CANH, CANL, 12V, GND, encoder A/B |
| Verification result | Matches schematic / differs from schematic |
| Action required | Update connector table if mismatch is found |

## Related documents

- [`../wiring_diagrams/connector_table.md`](../wiring_diagrams/connector_table.md)
- [`../wiring_diagrams/nodos_controladores.md`](../wiring_diagrams/nodos_controladores.md)
- [`../power_distribution/power_summary.md`](../power_distribution/power_summary.md)
- [`../schematics/schematics_index.md`](../schematics/schematics_index.md)

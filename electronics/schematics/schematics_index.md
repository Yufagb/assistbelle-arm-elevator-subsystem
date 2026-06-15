<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Schematics index

This document indexes the schematic PDFs for the Assistbelle robotic arm and elevator subsystem and records the electrical information extracted from each sheet.

## Schematic files

| File | Subsystem | Main blocks shown | Status |
|---|---|---|---|
| `DC_MOTOR_DRIVER_SCH.pdf` | DRV8871 DC motor controller node | ESP32 NodeMCU, SN65HVD230DR CAN transceiver, DRV8871DDA, power/CAN/motor headers. | Reviewed from uploaded PDF; physical wiring still pending. |
| `DC_MOTOR_DRIVER_SCH_IBT2.pdf` | IBT-2 DC motor controller node | ESP32 NodeMCU, SN65HVD230DR CAN transceiver, IBT-2 connector, power/CAN/motor headers. | Reviewed from uploaded PDF; physical wiring still pending. |
| `Main Bus.pdf` | Main power and CAN bus | 12 V, P_GND, 5 V, S_GND, CANH, CANL, RT1/RT2 120-ohm terminations and subsystem connectors. | Reviewed from uploaded PDF; physical implementation still pending. |
| `RASPBERRYPI_MCP2515.pdf` | Raspberry Pi to MCP2515 interface | Raspberry Pi 40-pin header, MCP2515 10-pin header, CAN connector and power connector. | Reviewed from uploaded PDF; module supply voltage must be verified. |
| `Stepper Driver v7.pdf` | J5 stepper/elevator controller | ESP32 NodeMCU, CAN transceiver, J_CAN, J_DRIVERS and J_5V connectors. | Reviewed from uploaded PDF; physical wiring still pending. |

## Extracted connector summary

| Schematic | Connector | Pin count | Signals / function | Notes |
|---|---|---:|---|---|
| `Main Bus.pdf` | `12V_PSU` | 2 | 12V, P_GND | Main actuator supply input. |
| `Main Bus.pdf` | `5V_PSU` | 2 | 5V, S_GND | Logic supply input. |
| `Main Bus.pdf` | `MCP_2515` | 2 | CANH, CANL | CAN branch for MCP2515. |
| `Main Bus.pdf` | `RPI_POWER` | 2 | 5V, S_GND | Raspberry Pi power branch. |
| `Main Bus.pdf` | `DCM_MOTOR_POWER` | 2 | 12V, P_GND | DC motor controller actuator power branch; used for four DC motor controllers. |
| `Main Bus.pdf` | `DCM_LOGIC_POWER` | 2 | 5V, S_GND | DC motor controller logic power branch. |
| `Main Bus.pdf` | `DCM_CAN_SN65H` | 2 | CANH, CANL | CAN branch for DC motor controller transceiver. |
| `Main Bus.pdf` | `STPR_LOGIC_POWER` | 2 | 5V, S_GND | Stepper/elevator logic power branch. |
| `Main Bus.pdf` | `STPR_CAN_SN65H` | 2 | CANH, CANL | CAN branch for stepper/elevator transceiver. |
| `DC_MOTOR_DRIVER_SCH.pdf` | `POWER_HEADERS` | 2 | 12V, GND | DRV8871 motor power. |
| `DC_MOTOR_DRIVER_SCH.pdf` | `J2` | 2 | 5V, GND | Logic power. |
| `DC_MOTOR_DRIVER_SCH.pdf` | `CAN_HEADER` | 2 | CANH, CANL | CAN bus connector. |
| `DC_MOTOR_DRIVER_SCH.pdf` | `MOTOR_HEADER` | 6 | M1, M2, 3V3, GND, ENCODER_A, ENCODER_B | Motor and encoder header. |
| `DC_MOTOR_DRIVER_SCH_IBT2.pdf` | `POWER_HEADERS` | 2 | 12V, GND | Board-level motor power header. |
| `DC_MOTOR_DRIVER_SCH_IBT2.pdf` | `J2` | 2 | 5V, GND | Logic power. |
| `DC_MOTOR_DRIVER_SCH_IBT2.pdf` | `CAN_HEADER` | 2 | CANH, CANL | CAN bus connector. |
| `DC_MOTOR_DRIVER_SCH_IBT2.pdf` | `MOTOR_HEADER` | 6 | M1, M2, 3V3, GND, ENCODER_A, ENCODER_B | Motor and encoder header. |
| `DC_MOTOR_DRIVER_SCH_IBT2.pdf` | `IBT2_CONN` | 8 | IN1, IN2, 5V, GND and IBT-2 control/interface pins | Exact pin order must be checked physically. |
| `DC_MOTOR_DRIVER_SCH_IBT2.pdf` | `IBT_POWER_HEADER` | 2 | 12V, GND | IBT-2 power branch. |
| `DC_MOTOR_DRIVER_SCH_IBT2.pdf` | `IBT_MOTOR_HEADER` | 2 | M1, M2 | Motor output branch. |
| `RASPBERRYPI_MCP2515.pdf` | `J_RPI` | 40 | Raspberry Pi GPIO header | Uses SPI and interrupt signals. |
| `RASPBERRYPI_MCP2515.pdf` | `J_MCP` | 10 | 3V3, GND, SCK, MOSI, MISO, CS_CAN, NC, INT_CAN, CANL, CANH | MCP2515-side header. |
| `RASPBERRYPI_MCP2515.pdf` | `J_CAN` | 2 | CANH, CANL | CAN bus connector. |
| `RASPBERRYPI_MCP2515.pdf` | `J_POWER` | 2 | 5V, GND | Power connector. |
| `Stepper Driver v7.pdf` | `J_CAN` | 2 | CANH, CANL | CAN bus connector. |
| `Stepper Driver v7.pdf` | `J_DRIVERS` | 3 | ENA, DIR, PUL | TB6600/elevator driver control. |
| `Stepper Driver v7.pdf` | `J_5V` | 2 | 5V, GND | Logic power connector. |

## Extracted component summary

| Schematic | Components identified |
|---|---|
| `DC_MOTOR_DRIVER_SCH.pdf` | ESP32 NodeMCU, SN65HVD230DR, DRV8871DDA, R1 20k on ILIM path. |
| `DC_MOTOR_DRIVER_SCH_IBT2.pdf` | ESP32 NodeMCU, SN65HVD230DR, IBT-2 interface connector. |
| `Main Bus.pdf` | Main six-line bus: 12V, P_GND, 5V, S_GND, CANH, CANL; two 120-ohm terminations RT1 and RT2. |
| `RASPBERRYPI_MCP2515.pdf` | Raspberry Pi 40-pin header, MCP2515 10-pin header, CAN connector and power connector. |
| `Stepper Driver v7.pdf` | ESP32 NodeMCU, CAN transceiver, J_CAN, J_DRIVERS and J_5V connectors. |

## Important verification notes

- `Main Bus.pdf` shows RT1 and RT2 as 120-ohm CAN terminations between CANH and CANL.
- `RASPBERRYPI_MCP2515.pdf` shows the MCP header using `3V3`, while a separate `J_POWER` connector provides `5V` and `GND`; the actual MCP2515 module voltage must be verified on the robot.
- `Stepper Driver v7.pdf` shows J5/elevator control signals `PUL`, `DIR` and `ENA`, and the visible ESP32 mapping is consistent with `PUL GPIO5`, `DIR GPIO18`, `ENA GPIO19`, `CAN_RX GPIO21`, and `CAN_TX GPIO22`.
- `DC_MOTOR_DRIVER_SCH.pdf` and `DC_MOTOR_DRIVER_SCH_IBT2.pdf` are generic controller-node schematics; final assignment to J1-J4 must be verified against the physical robot.

## Physical review checklist

- [ ] Confirm that the GitHub `electronics/schematics/` folder contains the same five PDFs listed above.
- [ ] Confirm if schematic PDFs are final exports or if editable KiCad/source files also exist.
- [ ] Confirm MCP2515 module voltage: 3.3 V or 5 V.
- [ ] Confirm CAN termination resistor locations RT1 and RT2 on the real wiring.
- [ ] Confirm connector pin order for all 2-pin, 3-pin, 6-pin, 8-pin and 10-pin connectors.
- [ ] Photograph each connector and driver board.
- [ ] Update `electronics/wiring_diagrams/connector_table.md` with final connector models, pin numbers, wire colors and cable gauges.

## Related documents

- [`../README.md`](../README.md)
- [`../pinout_tables/esp32_pinout_table.md`](../pinout_tables/esp32_pinout_table.md)
- [`../pinout_tables/raspberry_pi_mcp2515.md`](../pinout_tables/raspberry_pi_mcp2515.md)
- [`../wiring_diagrams/bus_principal.md`](../wiring_diagrams/bus_principal.md)
- [`../wiring_diagrams/connector_table.md`](../wiring_diagrams/connector_table.md)
- [`../power_distribution/power_summary.md`](../power_distribution/power_summary.md)

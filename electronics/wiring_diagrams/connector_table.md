<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Connector table

This file is the working connector table for the Assistbelle robotic arm and elevator subsystem. It combines information extracted from the schematic PDFs with fields that must still be verified physically on the robot.

## Status legend

| Mark | Meaning |
|---|---|
| Known from schematic | Value extracted from the uploaded schematic PDFs. |
| Known from docs | Value taken from repository documentation or firmware-derived pinout tables. |
| To verify | Value must be checked physically on the robot before HardwareX submission. |
| Unknown | Value is not available yet and must be filled from inspection, photos or measurements. |

## Main bus connector inventory

Extracted from `Main Bus.pdf`.

| Connector ID | Schematic connector | Subsystem | Pin count | Signals | Status | Notes |
|---|---|---|---:|---|---|---|
| C-MBUS-12V-IN | `12V_PSU` | Power supplies | 2 | 12V, P_GND | Known from schematic, wiring to verify | Input from Dell server PSU. |
| C-MBUS-5V-IN | `5V_PSU` | Power supplies | 2 | 5V, S_GND | Known from schematic, wiring to verify | Input from LM2596S 5 V logic rail. |
| C-MBUS-RPI-CAN | `MCP_2515` | Raspberry Pi connections | 2 | CANH, CANL | Known from schematic, wiring to verify | Branch to MCP2515 CAN module. |
| C-MBUS-RPI-PWR | `RPI_POWER` | Raspberry Pi connections | 2 | 5V, S_GND | Known from schematic, wiring to verify | Logic power branch to Raspberry Pi. |
| C-MBUS-DCM-PWR | `DCM_MOTOR_POWER` | DC motor controller x4 | 2 | 12V, P_GND | Known from schematic, wiring to verify | Actuator power branch for DC motor controllers. |
| C-MBUS-DCM-LOGIC | `DCM_LOGIC_POWER` | DC motor controller x4 | 2 | 5V, S_GND | Known from schematic, wiring to verify | Logic power branch for DC motor controllers. |
| C-MBUS-DCM-CAN | `DCM_CAN_SN65H` | DC motor controller x4 | 2 | CANH, CANL | Known from schematic, wiring to verify | CAN branch for DC motor-controller CAN transceiver. |
| C-MBUS-STPR-LOGIC | `STPR_LOGIC_POWER` | Stepper motor controller | 2 | 5V, S_GND | Known from schematic, wiring to verify | Logic power branch for stepper controller. |
| C-MBUS-STPR-CAN | `STPR_CAN_SN65H` | Stepper motor controller | 2 | CANH, CANL | Known from schematic, wiring to verify | CAN branch for stepper-controller CAN transceiver. |

Main Bus also shows two 120-ohm CAN terminations: `RT1` and `RT2`. Their physical location must be verified.

## Raspberry Pi to MCP2515 connector inventory

Extracted from `RASPBERRYPI_MCP2515.pdf` and updated with the confirmed implementation note that the MCP2515 module is powered from 5 V.

| Connector ID | Schematic connector | Subsystem | Pin count | Signals | Status | Notes |
|---|---|---|---:|---|---|---|
| C-RPI-GPIO | `J_RPI` | Raspberry Pi GPIO | 40 | 3V3, 5V, GND, MOSI, MISO, SCK, CS_CAN, INT_CAN | Known from schematic, wiring to verify | Raspberry Pi 40-pin header. SPI/INT signals must remain Raspberry Pi 3.3 V logic-compatible. |
| C-MCP-HEADER | `J_MCP` | MCP2515 module | 10 | 3V3, GND, SCK, MOSI, MISO, CS_CAN, NC, INT_CAN, CANL, CANH | Known from schematic, logic compatibility to verify | Schematic shows a 3V3 reference at the MCP header; final module power is 5 V through `J_POWER`. |
| C-MCP-CAN | `J_CAN` | CAN connector | 2 | CANH, CANL | Known from schematic, pin order to verify | CAN output from MCP2515 module. |
| C-MCP-PWR | `J_POWER` | MCP2515 module power | 2 | 5V, GND | Known from schematic and implementation | 5 V module power input. |

## DRV8871 DC motor controller connector inventory

Extracted from `DC_MOTOR_DRIVER_SCH.pdf`.

| Connector ID | Schematic connector | Subsystem | Pin count | Signals | Status | Notes |
|---|---|---|---:|---|---|---|
| C-DRV8871-PWR | `POWER_HEADERS` | DRV8871 motor power | 2 | 12V, GND | Known from schematic, wiring to verify | Motor-power input. |
| C-DRV8871-LOGIC | `J2` | Logic power | 2 | 5V, GND | Known from schematic, wiring to verify | Logic-power input. |
| C-DRV8871-CAN | `CAN_HEADER` | CAN connector | 2 | CANH, CANL | Known from schematic, wiring to verify | SN65HVD230DR CAN bus connector. |
| C-DRV8871-MOTOR | `MOTOR_HEADER` | Motor/encoder header | 6 | M1, M2, 3V3, GND, ENCODER_A, ENCODER_B | Known from schematic, pin order to verify | Motor output plus encoder supply/signals. |

Relevant components: ESP32 NodeMCU, SN65HVD230DR, DRV8871DDA and R1 20k on the ILIM path.

## IBT-2 DC motor controller connector inventory

Extracted from `DC_MOTOR_DRIVER_SCH_IBT2.pdf`.

| Connector ID | Schematic connector | Subsystem | Pin count | Signals | Status | Notes |
|---|---|---|---:|---|---|---|
| C-IBT2-PWR | `POWER_HEADERS` | Board motor power | 2 | 12V, GND | Known from schematic, wiring to verify | Board-level power header. |
| C-IBT2-LOGIC | `J2` | Logic power | 2 | 5V, GND | Known from schematic, wiring to verify | Logic-power input. |
| C-IBT2-CAN | `CAN_HEADER` | CAN connector | 2 | CANH, CANL | Known from schematic, wiring to verify | SN65HVD230DR CAN bus connector. |
| C-IBT2-MOTOR | `MOTOR_HEADER` | Motor/encoder header | 6 | M1, M2, 3V3, GND, ENCODER_A, ENCODER_B | Known from schematic, pin order to verify | Motor and encoder header. |
| C-IBT2-CTRL | `IBT2_CONN` | IBT-2 control interface | 8 | IN1, IN2, 5V, GND and additional IBT-2 interface pins | Known from schematic, exact pin order to verify | 2x4 header to IBT-2. |
| C-IBT2-POWER-OUT | `IBT_POWER_HEADER` | IBT-2 power branch | 2 | 12V, GND | Known from schematic, wiring to verify | Power branch to IBT-2. |
| C-IBT2-MOTOR-OUT | `IBT_MOTOR_HEADER` | IBT-2 motor branch | 2 | M1, M2 | Known from schematic, wiring to verify | Motor output branch. |

## Stepper / elevator connector inventory

Extracted from `Stepper Driver v7.pdf`.

| Connector ID | Schematic connector | Subsystem | Pin count | Signals | Status | Notes |
|---|---|---|---:|---|---|---|
| C-STPR-CAN | `J_CAN` | CAN connector | 2 | CANH, CANL | Known from schematic, pin order to verify | CAN bus for stepper/elevator controller. |
| C-STPR-DRV | `J_DRIVERS` | TB6600 driver control | 3 | ENA, DIR, PUL | Known from schematic, pin order to verify | Driver control interface. |
| C-STPR-5V | `J_5V` | Logic power | 2 | 5V, GND | Known from schematic, wiring to verify | Logic-power input. |

Visible ESP32 signal mapping from the schematic:

| Signal | ESP32 GPIO | Status |
|---|---:|---|
| PUL | GPIO5 | Known from schematic; verify physically. |
| DIR | GPIO18 | Known from schematic; verify physically. |
| ENA | GPIO19 | Known from schematic; verify physically. |
| CAN_RX | GPIO21 | Known from schematic; verify physically. |
| CAN_TX | GPIO22 | Known from schematic; verify physically. |

## Joint-to-driver assignment to verify

| Joint | Current documented driver | Schematic source | Verification status |
|---|---|---|---|
| J1 | DRV8871 | `DC_MOTOR_DRIVER_SCH.pdf` | To verify physically. |
| J2 | IBT-2 | `DC_MOTOR_DRIVER_SCH_IBT2.pdf` | To verify physically. |
| J3 | IBT-2 | `DC_MOTOR_DRIVER_SCH_IBT2.pdf` | To verify physically. |
| J4 | DRV8871 + gripper servo | `DC_MOTOR_DRIVER_SCH.pdf` plus gripper wiring | To verify physically. |
| J5 | TB6600 / stepper driver | `Stepper Driver v7.pdf` | To verify physically. |

## Physical verification checklist

Use this checklist during the next robot access session.

- [ ] Take a general photo of the electronics layout.
- [ ] Take one close-up photo of the Dell server power supply label.
- [ ] Record the exact Dell power-supply model.
- [ ] Take one photo of the LM2596S DC-DC converter and its wiring.
- [ ] Confirm 5 V output with a multimeter before connecting logic loads.
- [ ] Take one photo of the panic-button wiring.
- [ ] Confirm that the panic button cuts actuator power only.
- [ ] Confirm Raspberry Pi and ESP32 nodes remain powered after panic-button activation.
- [ ] Photograph CAN bus termination resistors RT1 and RT2.
- [ ] Confirm CANH/CANL connector orientation.
- [ ] Confirm MCP2515 module receives 5 V power and is safe for Raspberry Pi 3.3 V SPI/INT signals.
- [ ] Photograph J1 driver and connector.
- [ ] Photograph J2 driver and connector.
- [ ] Photograph J3 driver and connector.
- [ ] Photograph J4 driver and connector.
- [ ] Photograph J5 TB6600 driver and connector.
- [ ] Record connector type/model if visible.
- [ ] Record pin count and wire color for each connector.
- [ ] Update this file with verified pinouts.

## Information still missing

- Exact connector models or terminal-block types.
- Exact physical pin order for each connector.
- Wire colors.
- Cable gauges for logic, CAN and driver control signals.
- Exact Dell server power-supply model.
- Physical location of CAN termination resistors RT1 and RT2.
- Exact MCP2515 module model or evidence that it is safe with Raspberry Pi 3.3 V SPI/INT logic while powered from 5 V.
- Final ground-bonding or isolation detail between Power GND and Signal GND.
- Final photos for `electronics/images/`.

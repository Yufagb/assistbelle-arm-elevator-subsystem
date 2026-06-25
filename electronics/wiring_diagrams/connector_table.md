<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Connector table

This file is the working connector table for the Assistbelle robotic arm and elevator subsystem. It combines information extracted from the schematic PDFs, repository documentation, firmware-derived pinout tables and user-confirmed design intent. Fields that require inspection of the physical robot remain explicitly marked as deferred or to verify.

## Status legend

| Mark | Meaning |
|---|---|
| Known from schematic | Value extracted from the uploaded schematic PDFs. |
| Known from docs | Value taken from repository documentation or firmware-derived pinout tables. |
| User-confirmed design intent | Confirmed by the project owner as intended architecture; physical wiring may still need verification. |
| Deferred physical verification | Must be checked when the physical robot is accessible again. |
| Unknown | Value is not available yet and must be filled from inspection, photos or measurements. |

## User-confirmed design decisions

| Topic | Confirmed decision | Remaining verification |
|---|---|---|
| J5 dual TB6600 control | The two TB6600 drivers receive the same `PUL`, `DIR` and `ENA` signals in parallel so the two NEMA 23 motors move synchronously. | Confirm physical wiring and terminal order. |
| J5 TB6600 actuator supply | Supply voltage still pending physical inspection. | Confirm whether both TB6600 drivers are powered from the Dell 12 V PSU or another rail. |
| MCP2515 power | MCP2515 module is powered from 5 V. | Confirm exact module model and 3.3 V SPI/INT compatibility with Raspberry Pi. |
| Emergency / panic button | Panic button cuts only actuator-side 12 V power; Raspberry Pi, ESP32 nodes and 5 V logic remain powered. | Photograph final panic-button wiring path. |
| CAN termination | RT1 and RT2 are intended as 120-ohm terminations at the two physical ends of the CAN bus. | Confirm physical resistor locations. |

## Main bus connector inventory

Extracted from `Main Bus.pdf`.

| Connector ID | Schematic connector | Subsystem | Pin count | Signals | Status | Notes |
|---|---|---|---:|---|---|---|
| C-MBUS-12V-IN | `12V_PSU` | Power supplies | 2 | 12V, P_GND | Known from schematic; deferred physical verification | Input from Dell server PSU. Exact PSU model and final wiring photo pending. |
| C-MBUS-5V-IN | `5V_PSU` | Power supplies | 2 | 5V, S_GND | Known from schematic; deferred physical verification | Input from LM2596S 5 V logic rail. |
| C-MBUS-RPI-CAN | `MCP_2515` | Raspberry Pi connections | 2 | CANH, CANL | Known from schematic; deferred physical verification | Branch to MCP2515 CAN module. |
| C-MBUS-RPI-PWR | `RPI_POWER` | Raspberry Pi connections | 2 | 5V, S_GND | Known from schematic and design intent | Logic power branch to Raspberry Pi; remains powered during emergency stop. |
| C-MBUS-DCM-PWR | `DCM_MOTOR_POWER` | DC motor controller x4 | 2 | 12V, P_GND | Known from schematic; deferred physical verification | Actuator power branch for DC motor controllers; interrupted by panic button by design. |
| C-MBUS-DCM-LOGIC | `DCM_LOGIC_POWER` | DC motor controller x4 | 2 | 5V, S_GND | Known from schematic and design intent | Logic power branch for DC motor controllers; remains powered during emergency stop. |
| C-MBUS-DCM-CAN | `DCM_CAN_SN65H` | DC motor controller x4 | 2 | CANH, CANL | Known from schematic; deferred physical verification | CAN branch for DC motor-controller CAN transceiver. |
| C-MBUS-STPR-LOGIC | `STPR_LOGIC_POWER` | Stepper motor controller | 2 | 5V, S_GND | Known from schematic and design intent | Logic power branch for J5/elevator controller; remains powered during emergency stop. |
| C-MBUS-STPR-CAN | `STPR_CAN_SN65H` | Stepper motor controller | 2 | CANH, CANL | Known from schematic; deferred physical verification | CAN branch for J5/elevator controller. |

Main Bus also shows two 120-ohm CAN terminations: `RT1` and `RT2`. They are intended to be placed at the two physical ends of the CAN bus; exact physical locations remain deferred until robot access.

## Raspberry Pi to MCP2515 connector inventory

Extracted from `RASPBERRYPI_MCP2515.pdf` and updated with the confirmed implementation note that the MCP2515 module is powered from 5 V.

| Connector ID | Schematic connector | Subsystem | Pin count | Signals | Status | Notes |
|---|---|---|---:|---|---|---|
| C-RPI-GPIO | `J_RPI` | Raspberry Pi GPIO | 40 | 3V3, 5V, GND, MOSI, MISO, SCK, CS_CAN, INT_CAN | Known from schematic, wiring to verify | Raspberry Pi 40-pin header. SPI/INT signals must remain Raspberry Pi 3.3 V logic-compatible. |
| C-MCP-HEADER | `J_MCP` | MCP2515 module | 10 | 3V3, GND, SCK, MOSI, MISO, CS_CAN, NC, INT_CAN, CANL, CANH | Known from schematic, logic compatibility to verify | Schematic shows a 3V3 reference at the MCP header; final module power is 5 V through `J_POWER`. |
| C-MCP-CAN | `J_CAN` | CAN connector | 2 | CANH, CANL | Known from schematic, pin order to verify | CAN output from MCP2515 module. |
| C-MCP-PWR | `J_POWER` | MCP2515 module power | 2 | 5V, GND | Known from schematic and user-confirmed design intent | 5 V module power input. |

## DRV8871 DC motor controller connector inventory

Extracted from `DC_MOTOR_DRIVER_SCH.pdf`.

| Connector ID | Schematic connector | Subsystem | Pin count | Signals | Status | Notes |
|---|---|---|---:|---|---|---|
| C-DRV8871-PWR | `POWER_HEADERS` | DRV8871 motor power | 2 | 12V, GND | Known from schematic; deferred physical verification | Motor-power input; actuator-side supply is interrupted by the panic button by design. |
| C-DRV8871-LOGIC | `J2` | Logic power | 2 | 5V, GND | Known from schematic; deferred physical verification | Logic-power input; logic remains powered during panic-button activation by design. |
| C-DRV8871-CAN | `CAN_HEADER` | CAN connector | 2 | CANH, CANL | Known from schematic; deferred physical verification | SN65HVD230DR CAN bus connector. |
| C-DRV8871-MOTOR | `MOTOR_HEADER` | Motor/encoder header | 6 | M1, M2, 3V3, GND, ENCODER_A, ENCODER_B | Known from schematic, pin order to verify | Motor output plus encoder supply/signals. |

Relevant components: ESP32 NodeMCU, SN65HVD230DR, DRV8871DDA and R1 20k on the ILIM path.

## IBT-2 DC motor controller connector inventory

Extracted from `DC_MOTOR_DRIVER_SCH_IBT2.pdf`.

| Connector ID | Schematic connector | Subsystem | Pin count | Signals | Status | Notes |
|---|---|---|---:|---|---|---|
| C-IBT2-PWR | `POWER_HEADERS` | Board motor power | 2 | 12V, GND | Known from schematic; deferred physical verification | Board-level motor-power header; actuator-side supply is interrupted by the panic button by design. |
| C-IBT2-LOGIC | `J2` | Logic power | 2 | 5V, GND | Known from schematic; deferred physical verification | Logic-power input; logic remains powered during panic-button activation by design. |
| C-IBT2-CAN | `CAN_HEADER` | CAN connector | 2 | CANH, CANL | Known from schematic; deferred physical verification | SN65HVD230DR CAN bus connector. |
| C-IBT2-MOTOR | `MOTOR_HEADER` | Motor/encoder header | 6 | M1, M2, 3V3, GND, ENCODER_A, ENCODER_B | Known from schematic, pin order to verify | Motor and encoder header. |
| C-IBT2-CTRL | `IBT2_CONN` | IBT-2 control interface | 8 | IN1, IN2, 5V, GND and additional IBT-2 interface pins | Known from schematic, exact pin order to verify | 2x4 header to IBT-2. For J2/J3, IBT-2 use is user-confirmed; physical pin order and enable wiring remain deferred. |
| C-IBT2-POWER-OUT | `IBT_POWER_HEADER` | IBT-2 power branch | 2 | 12V, GND | Known from schematic; deferred physical verification | Power branch to IBT-2. |
| C-IBT2-MOTOR-OUT | `IBT_MOTOR_HEADER` | IBT-2 motor branch | 2 | M1, M2 | Known from schematic; deferred physical verification | Motor output branch. |

## Stepper / elevator connector inventory

Extracted from `Stepper Driver v7.pdf` and user-confirmed J5 dual-driver architecture.

| Connector ID | Schematic connector | Subsystem | Pin count | Signals | Status | Notes |
|---|---|---|---:|---|---|---|
| C-STPR-CAN | `J_CAN` | CAN connector | 2 | CANH, CANL | Known from schematic, pin order to verify | CAN bus for stepper/elevator controller. |
| C-STPR-DRV | `J_DRIVERS` | TB6600 driver control | 3 | ENA, DIR, PUL | Known from schematic and firmware | Driver control interface from ESP32. In the current design intent, these signals are distributed in parallel to two TB6600 drivers. |
| C-STPR-5V | `J_5V` | Logic power | 2 | 5V, GND | Known from schematic and design intent | Logic-power input for the J5 controller; remains powered during panic-button activation. |
| C-STPR-TB6600-A-CTRL | TB6600 Motor A control terminals | J5 TB6600 Motor A | 3 | PUL, DIR, ENA | User-confirmed design intent; deferred physical verification | Receives ESP32 `PUL`, `DIR` and `ENA` in parallel with Motor B driver. |
| C-STPR-TB6600-B-CTRL | TB6600 Motor B control terminals | J5 TB6600 Motor B | 3 | PUL, DIR, ENA | User-confirmed design intent; deferred physical verification | Receives ESP32 `PUL`, `DIR` and `ENA` in parallel with Motor A driver. |
| C-STPR-TB6600-A-PWR | TB6600 Motor A power terminals | J5 TB6600 Motor A | 2 | VMOT, GND | Deferred physical verification | Supply voltage pending physical inspection. |
| C-STPR-TB6600-B-PWR | TB6600 Motor B power terminals | J5 TB6600 Motor B | 2 | VMOT, GND | Deferred physical verification | Supply voltage pending physical inspection. |

Visible ESP32 signal mapping from the schematic and firmware:

| Signal | ESP32 GPIO | Status |
|---|---:|---|
| PUL | GPIO5 | Known from schematic and firmware; verify physically. |
| DIR | GPIO18 | Known from schematic and firmware; verify physically. |
| ENA | GPIO19 | Known from schematic and firmware; verify physically. |
| CAN_RX | GPIO21 | Known from schematic and firmware; verify physically. |
| CAN_TX | GPIO22 | Known from schematic and firmware; verify physically. |

## Joint-to-driver assignment to verify

| Joint | Current documented driver | Schematic source | Verification status |
|---|---|---|---|
| J1 | DRV8871 | `DC_MOTOR_DRIVER_SCH.pdf` | To verify physically. |
| J2 | IBT-2 | `DC_MOTOR_DRIVER_SCH_IBT2.pdf` | User-confirmed driver family; physical wiring to verify. |
| J3 | IBT-2 | `DC_MOTOR_DRIVER_SCH_IBT2.pdf` | User-confirmed driver family; physical wiring to verify. |
| J4 | DRV8871 + gripper servo | `DC_MOTOR_DRIVER_SCH.pdf` plus gripper wiring | To verify physically. |
| J5 | Two TB6600 drivers controlling two NEMA 23 motors | `Stepper Driver v7.pdf` plus user-confirmed design intent | Dual-driver parallel `PUL`/`DIR`/`ENA` design confirmed; physical wiring and supply voltage to verify. |

## Physical verification checklist

Use this checklist during the next robot access session.

- [ ] Take a general photo of the electronics layout.
- [ ] Take one close-up photo of the Dell server power supply label.
- [ ] Record the exact Dell power-supply model.
- [ ] Confirm the supply voltage used by both J5 TB6600 drivers.
- [ ] Take one photo of the LM2596S DC-DC converter and its wiring.
- [ ] Confirm 5 V output with a multimeter before connecting logic loads.
- [ ] Take one photo of the panic-button wiring.
- [x] Confirm design intent: panic button cuts actuator power only.
- [ ] Confirm physically that the panic button cuts actuator power only.
- [x] Confirm design intent: Raspberry Pi and ESP32 nodes remain powered after panic-button activation.
- [ ] Confirm physically that Raspberry Pi and ESP32 nodes remain powered after panic-button activation.
- [ ] Photograph CAN bus termination resistors RT1 and RT2.
- [x] Confirm design intent: RT1 and RT2 are 120-ohm terminations at the physical ends of the CAN bus.
- [ ] Confirm physical location of RT1 and RT2.
- [ ] Confirm CANH/CANL connector orientation.
- [x] Confirm MCP2515 module receives 5 V power in the design.
- [ ] Confirm physically that MCP2515 module receives 5 V power.
- [ ] Confirm the specific MCP2515 module used is safe for Raspberry Pi 3.3 V SPI/INT logic.
- [ ] Photograph J1 driver and connector.
- [ ] Photograph J2 IBT-2 driver and connector.
- [ ] Photograph J3 IBT-2 driver and connector.
- [ ] Photograph J4 driver and connector.
- [ ] Photograph both J5 TB6600 drivers and connectors.
- [ ] Record connector type/model if visible.
- [ ] Record pin count and wire color for each connector.
- [ ] Update this file with verified pinouts.

## Information still missing

- Exact connector models or terminal-block types.
- Exact physical pin order for each connector.
- Wire colors.
- Cable gauges for logic, CAN and driver control signals.
- Exact Dell server power-supply model.
- TB6600 supply voltage for the two J5 drivers.
- Physical location of CAN termination resistors RT1 and RT2.
- Exact MCP2515 module model or evidence that it is safe with Raspberry Pi 3.3 V SPI/INT logic while powered from 5 V.
- Final ground-bonding or isolation detail between Power GND and Signal GND.
- Final photos for `electronics/images/`.

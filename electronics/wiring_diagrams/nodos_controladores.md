<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Controller nodes

This document summarizes the controller-node architecture for the Assistbelle robotic arm and elevator subsystem.

## Scope

The controller nodes described here correspond to the robotic arm and vertical elevator subsystem. The information is based on the thesis diagrams, firmware pinout documentation, current design notes and user-confirmed build information. Final photos and connector-level pin verification are still required before publication.

## General architecture

The subsystem uses distributed ESP32-based controller nodes connected through CAN using SN65HVD230D CAN transceivers.

| Node | Actuator / subsystem | Current documented driver | Main function | Verification status |
|---|---|---|---|---|
| J1 / Node 1 | Joint 1 / base | DRV8871 | DC motor with quadrature encoder. | Documentation pending: board photo and wiring check. |
| J2 / Node 2 | Joint 2 / shoulder | IBT-2 | DC motor with quadrature encoder. | User-confirmed active; photo and wiring check pending. |
| J3 / Node 3 | Joint 3 / elbow | IBT-2 | DC motor with quadrature encoder. | User-confirmed active; photo and wiring check pending. |
| J4 / Node 4 | Joint 4 / wrist + gripper | DRV8871 + servo | DC motor with encoder and gripper servo control. | Documentation pending: board photo and wiring check. |
| J5 / Node 5 | Vertical elevator / prismatic axis | TB6600 | Stepper motor control for elevator motion. | Documentation pending: board photo and wiring check. |

## Current driver assignment

The current documentation should use the following driver assignment:

| Joint | Driver | Notes |
|---|---|---|
| J1 | DRV8871 | Base joint. |
| J2 | IBT-2 | Shoulder joint; user-confirmed IBT-2 implementation; self-locking mechanical behavior reported when actuator power is cut. |
| J3 | IBT-2 | Elbow joint; user-confirmed IBT-2 implementation; self-locking mechanical behavior reported when actuator power is cut. |
| J4 | DRV8871 + servo | Wrist motor plus gripper servo. |
| J5 | TB6600 | Vertical elevator / prismatic axis. |

## DRV8871-based DC node

The DRV8871-based node is used for J1 and J4 in the current documentation.

Main signals:

| Signal | Function |
|---|---|
| IN1 / PWM control | Motor-drive control input. |
| IN2 / direction control | Motor-drive control input. |
| Encoder A | Quadrature encoder phase A. |
| Encoder B | Quadrature encoder phase B. |
| CAN TX/RX | ESP32 logic communication to CAN transceiver. |
| CANH/CANL | Differential CAN bus lines. |
| 12 V | Motor power rail. |
| 5 V / 3.3 V | Logic rail, depending on module requirements. |
| GND | Ground reference according to the power-distribution strategy. |

## IBT-2-based DC node

The IBT-2-based node is used for J2 and J3. This assignment has been confirmed by the user during the project review, but board photos and exact connector pin mapping are still required for HardwareX publication.

Main signals:

| Signal | Function |
|---|---|
| RPWM | PWM command for one motor direction. |
| LPWM | PWM command for the opposite motor direction. |
| R_EN | Right-side bridge enable. |
| L_EN | Left-side bridge enable. |
| Encoder A | Quadrature encoder phase A. |
| Encoder B | Quadrature encoder phase B. |
| CAN TX/RX | ESP32 logic communication to CAN transceiver. |
| CANH/CANL | Differential CAN bus lines. |
| 12 V | Motor power rail. |
| GND | Ground reference according to the power-distribution strategy. |

Firmware review note: current J2/J3 source definitions expose generic `DRV_IN1` and `DRV_IN2` names. During firmware review, verify whether these map to IBT-2 `RPWM`/`LPWM` with enable pins tied high, or whether firmware must explicitly define `RPWM`, `LPWM`, `R_EN` and `L_EN`.

## TB6600 elevator node

The TB6600-based node is used for the vertical elevator / prismatic axis J5.

Main signals:

| Signal | Function |
|---|---|
| STEP / PUL | Step pulse signal. |
| DIR | Direction signal. |
| EN / ENA | Driver enable signal. |
| CAN TX/RX | ESP32 logic communication to CAN transceiver. |
| CANH/CANL | Differential CAN bus lines. |
| 12 V | Stepper-driver power rail. |
| 5 V | Logic rail. |
| GND | Ground reference according to the power-distribution strategy. |

## Validation checklist for next hardware access

- [ ] Photograph J1 DRV8871 board and wiring.
- [ ] Photograph J2 IBT-2 board and wiring.
- [ ] Photograph J3 IBT-2 board and wiring.
- [ ] Photograph J4 DRV8871 board, wrist motor wiring and gripper servo wiring.
- [ ] Photograph J5 TB6600 board and wiring.
- [ ] Confirm whether J2/J3 IBT-2 enable pins are tied high or controlled by ESP32 GPIO.
- [ ] Confirm power connections: actuator rail, logic rail and grounds.
- [ ] Confirm CAN TX/RX mapping against `electronics/pinout_tables/esp32_pinout_table.md`.
- [ ] Update this document if the physical robot differs from the current documented assignment.

## Related documents

- [`../pinout_tables/esp32_pinout_table.md`](../pinout_tables/esp32_pinout_table.md)
- [`../power_distribution/power_summary.md`](../power_distribution/power_summary.md)
- [`bus_principal.md`](bus_principal.md)
- [`../schematics/schematics_index.md`](../schematics/schematics_index.md)

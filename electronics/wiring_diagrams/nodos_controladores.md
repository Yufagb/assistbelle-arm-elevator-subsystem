<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Controller nodes

This document summarizes the controller-node architecture for the Assistbelle robotic arm and elevator subsystem.

## Scope

The controller nodes described here correspond to the robotic arm and vertical elevator subsystem. The information is based on the thesis diagrams, firmware pinout documentation and the current design notes. The physical driver assignment must be verified on the robot during the next hardware access session.

## General architecture

The subsystem uses distributed ESP32-based controller nodes connected through CAN using SN65HVD230D CAN transceivers.

| Node | Actuator / subsystem | Current documented driver | Main function | Verification status |
|---|---|---|---|---|
| J1 / Node 1 | Joint 1 / base | DRV8871 | DC motor with quadrature encoder. | To be physically verified. |
| J2 / Node 2 | Joint 2 / shoulder | IBT-2 | DC motor with quadrature encoder. | To be physically verified. |
| J3 / Node 3 | Joint 3 / elbow | IBT-2 | DC motor with quadrature encoder. | To be physically verified. |
| J4 / Node 4 | Joint 4 / wrist + gripper | DRV8871 + servo | DC motor with encoder and gripper servo control. | To be physically verified. |
| J5 / Node 5 | Vertical elevator / prismatic axis | TB6600 | Stepper motor control for elevator motion. | To be physically verified. |

## Current driver assignment

The current documentation should use the following driver assignment until the physical inspection is completed:

| Joint | Driver | Notes |
|---|---|---|
| J1 | DRV8871 | Base joint. |
| J2 | IBT-2 | Shoulder joint; self-locking mechanical behavior reported when actuator power is cut. |
| J3 | IBT-2 | Elbow joint; self-locking mechanical behavior reported when actuator power is cut. |
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

The IBT-2-based node is documented for J2 and J3. This must be verified physically before final HardwareX submission.

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

- [ ] Confirm visually that J1 uses DRV8871.
- [ ] Confirm visually that J2 uses IBT-2.
- [ ] Confirm visually that J3 uses IBT-2.
- [ ] Confirm visually that J4 uses DRV8871 and a gripper servo.
- [ ] Confirm visually that J5 uses TB6600.
- [ ] Photograph each controller node.
- [ ] Photograph wiring from ESP32 to driver for each node.
- [ ] Confirm power connections: actuator rail, logic rail and grounds.
- [ ] Confirm CAN TX/RX mapping against `electronics/pinout_tables/esp32_pinout_table.md`.
- [ ] Update this document if the physical robot differs from the current documented assignment.

## Related documents

- [`../pinout_tables/esp32_pinout_table.md`](../pinout_tables/esp32_pinout_table.md)
- [`../power_distribution/power_summary.md`](../power_distribution/power_summary.md)
- [`bus_principal.md`](bus_principal.md)
- [`../schematics/schematics_index.md`](../schematics/schematics_index.md)

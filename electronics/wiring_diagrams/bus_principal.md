<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Main bus wiring diagram

This document describes the main power and CAN bus of the Assistbelle robotic arm and elevator subsystem based on the reviewed `Main Bus.pdf` schematic.

## Source schematic

| File | Description | Status |
|---|---|---|
| [`../schematics/Main Bus.pdf`](../schematics/Main%20Bus.pdf) | Main 12 V / 5 V / CAN distribution bus. | Reviewed from PDF; physical implementation still pending. |

## Bus lines

The main bus distributes power and communication through six labeled lines.

| Line | Function | Domain | Notes |
|---|---|---|---|
| `12V` | Actuator power rail. | Power | Feeds motor drivers and actuator-side loads. |
| `P_GND` | Power ground. | Power | Return path for actuator/motor power. |
| `5V` | Logic power rail. | Signal / logic | Feeds Raspberry Pi, ESP32 nodes and CAN-related logic. |
| `S_GND` | Signal ground. | Signal / logic | Reference for logic, CAN transceivers and telemetry electronics. |
| `CANH` | CAN high differential line. | Communication | Pair with CANL. |
| `CANL` | CAN low differential line. | Communication | Pair with CANH. |

The current documentation treats `P_GND` and `S_GND` as separated domains. Their final physical bonding or isolation strategy must be verified on the robot.

## Connector groups from `Main Bus.pdf`

| Group | Schematic connector | Pin count | Signals | Purpose | Verification status |
|---|---|---:|---|---|---|
| `POWER_SUPPLIES` | `12V_PSU` | 2 | `12V`, `P_GND` | Main actuator-supply input. | Wiring and Dell PSU model pending. |
| `POWER_SUPPLIES` | `5V_PSU` | 2 | `5V`, `S_GND` | Logic-supply input from DC-DC converter. | Wiring and converter placement pending. |
| `RPI_CONNECTIONS` | `MCP_2515` | 2 | `CANH`, `CANL` | CAN branch to the Raspberry Pi/MCP2515 interface. | Pin order pending. |
| `RPI_CONNECTIONS` | `RPI_POWER` | 2 | `5V`, `S_GND` | Logic power branch for Raspberry Pi side. | Physical wiring pending. |
| `DC_MOTOR_CONTROLLER_X4` | `DCM_MOTOR_POWER` | 2 | `12V`, `P_GND` | Actuator power for four DC motor-controller branches. | Physical branching pending. |
| `DC_MOTOR_CONTROLLER_X4` | `DCM_LOGIC_POWER` | 2 | `5V`, `S_GND` | Logic power for DC motor-controller nodes. | Physical branching pending. |
| `DC_MOTOR_CONTROLLER_X4` | `DCM_CAN_SN65H` | 2 | `CANH`, `CANL` | CAN branch for DC motor-controller transceivers. | Physical branching pending. |
| `STEPPER_MOTOR_CONTROLLER` | `STPR_LOGIC_POWER` | 2 | `5V`, `S_GND` | Logic power for the J5/elevator controller. | Physical wiring pending. |
| `STEPPER_MOTOR_CONTROLLER` | `STPR_CAN_SN65H` | 2 | `CANH`, `CANL` | CAN branch for the J5/elevator controller. | Physical wiring pending. |

## CAN termination

The reviewed schematic shows two 120-ohm CAN termination resistors:

| Reference | Value | Location in schematic | Physical status |
|---|---:|---|---|
| `RT1` | 120 ohm | One end of the CAN bus, between `CANH` and `CANL`. | To verify physically. |
| `RT2` | 120 ohm | Opposite end of the CAN bus, between `CANH` and `CANL`. | To verify physically. |

Implementation rule:

- place one 120-ohm termination between `CANH` and `CANL` at the beginning of the bus;
- place one 120-ohm termination between `CANH` and `CANL` at the end of the bus;
- avoid additional intermediate terminations on branch nodes unless the physical bus topology requires a documented change.

## Relationship with the current power architecture

The current hardware notes define:

| Block | Current documented implementation |
|---|---|
| Main actuator supply | Dell server power supply, 12 V, 1 kW, 88 A, exact model pending. |
| Logic supply | LM2596S DC-DC buck converter, 24 V / 12 V input to 5 V, 5 A output. |
| Emergency / panic button | Cuts actuator power while Raspberry Pi, ESP32 nodes and CAN/telemetry remain powered. |
| Grounds | `P_GND` and `S_GND` documented as separated domains. |

The panic-button wiring path is not shown explicitly in `Main Bus.pdf`; it must be documented with a photo or updated schematic before final publication.

## Recommended wiring notes

These notes should be verified against the physical implementation:

- use higher-current wiring for `12V` and `P_GND` actuator branches;
- use logic-rated wiring for `5V` and `S_GND` branches;
- use a twisted pair for `CANH` and `CANL`;
- keep CAN stubs as short as practical;
- label `CANH` and `CANL` consistently across every connector;
- keep connector orientation visible in the final photos.

## Physical verification checklist

- [ ] Photograph the full main bus wiring.
- [ ] Photograph the Dell server power-supply connection to `12V_PSU`.
- [ ] Photograph the LM2596S output wiring to `5V_PSU`.
- [ ] Confirm the exact physical location of `RT1`.
- [ ] Confirm the exact physical location of `RT2`.
- [ ] Verify that `CANH` and `CANL` are not swapped in any branch.
- [ ] Confirm whether `P_GND` and `S_GND` remain separated or are bonded at one defined point.
- [ ] Document the panic-button actuator-power cut-off path.
- [ ] Update [`connector_table.md`](connector_table.md) with connector model, pin order, wire color and cable gauge.

## Related documents

- [`../schematics/schematics_index.md`](../schematics/schematics_index.md)
- [`connector_table.md`](connector_table.md)
- [`nodos_controladores.md`](nodos_controladores.md)
- [`../power_distribution/power_summary.md`](../power_distribution/power_summary.md)
- [`../images/README.md`](../images/README.md)

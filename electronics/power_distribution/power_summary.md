<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Power distribution summary

This document summarizes the current power-distribution architecture for the Assistbelle robotic arm and elevator subsystem.

## Scope

The power system described here covers the arm and vertical elevator subsystem only. It does not describe the complete mobile base, autonomous navigation electronics, storage module or any clinical deployment configuration.

## Power architecture

| Rail / block | Nominal value | Function | Current status |
|---|---:|---|---|
| Main actuator supply | 12 V nominal | Power for actuators, motor drivers and high-current loads. | Final architecture uses a Dell server power supply; exact model pending. TB6600 supply voltage to be confirmed physically. |
| Main supply rating | 1 kW, 88 A, 12 V | Available high-current supply for actuator power bus. | Model to be specified. |
| Logic supply | 5 V, 5 A | Raspberry Pi, ESP32 nodes and low-power logic peripherals. | Generated with LM2596S DC-DC buck converter module. |
| DC-DC converter input | 24 V / 12 V input compatible | Step-down input range for the LM2596S module. | Used to generate the 5 V logic rail. |
| CAN bus | Differential CANH/CANL | Communication between Raspberry Pi/MCP2515 and ESP32 nodes. | Uses common reference through signal-side ground. |

## Grounding strategy

The implementation separates the high-current power ground and the signal-side ground:

| Ground line | Description | Notes |
|---|---|---|
| Power GND | Return path from the actuator supply. | Associated with motor drivers and actuator power. |
| Signal GND | Return/reference for the 5 V logic rail from the DC-DC converter. | Associated with Raspberry Pi, ESP32 nodes, CAN transceivers and telemetry. |

The power and signal grounds are intentionally documented as separate domains in the current architecture. Any final single-point bonding, isolation strategy or measurement reference should be verified and documented before publication.

## Emergency stop / panic button behavior

The user-confirmed design intent is that the panic button cuts actuator power while keeping the logic and telemetry electronics powered.

| Subsystem | Behavior when panic button is activated |
|---|---|
| Actuator power rail | Interrupted. Motor drivers and actuators stop receiving actuator-side power. |
| Raspberry Pi | Remains powered from the 5 V logic rail. |
| ESP32 nodes | Remain powered from the 5 V logic rail. |
| CAN/telemetry | Remains available for diagnostics and code testing. |
| J2 and J3 | Mechanically self-locking, so the arm does not lose position when actuator power is removed. |

This architecture allows safer intervention while preserving communication, telemetry and debugging capability.

## J5 elevator driver power note

The elevator uses two TB6600 drivers for two NEMA 23 motors. The user-confirmed control design sends the same `PUL`, `DIR` and `ENA` signals to both drivers in parallel. The supply voltage used by the two TB6600 drivers is still pending physical inspection and must be confirmed before final HardwareX submission.

## Removed power options

LiPo batteries are not part of the current public HardwareX package and should not be considered part of the active BOM or final reproducible configuration.

| Item | Status |
|---|---|
| LiPo battery pack | Removed from active design and BOM. |
| Battery-powered operation | Out of current public package scope. |

## Related components

| Component | Role | Status |
|---|---|---|
| Dell server power supply | 12 V, 1 kW, 88 A actuator supply. | Exact model pending. |
| LM2596S buck converter module | DC-DC 24 V / 12 V to 5 V, 5 A. | Used for logic rail. |
| Raspberry Pi 5 | Main computer / ROS 2 side. | Powered by logic rail. |
| ESP32 DevKitC nodes | Distributed control nodes. | Powered by logic rail. |
| MCP2515 CAN-SPI module | Raspberry Pi CAN interface. | Powered from 5 V by design; Raspberry Pi 3.3 V SPI/INT compatibility must be verified by module selection. |
| SN65HVD230 CAN transceivers | CAN physical layer. | Powered from logic side. |
| DRV8871 drivers | DC motor actuation. | Powered from actuator rail. |
| IBT-2 / BTS7960 drivers | J2/J3 DC motor actuation. | Powered from actuator rail; physical wiring to verify. |
| TB6600 drivers | J5/elevator stepper actuation. | Supply voltage pending physical inspection. |

## Publication notes

Before final HardwareX submission, the following information should be added or confirmed:

- exact Dell server power-supply model;
- supply voltage used by the two J5 TB6600 drivers;
- measured current draw of the actuator rail during representative tests;
- measured current draw of the 5 V logic rail;
- wiring diagram showing the panic-button cut-off path;
- final location of the LM2596S module;
- final ground-bonding or isolation strategy;
- photographs of the power supply, converter, panic button and wiring harness.

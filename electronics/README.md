<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Electronics

Electrical and electronics documentation for the Assistbelle robotic arm and elevator subsystem.

## Index

- [Folder map](#folder-map)
- [Current status](#current-status)
- [Main documents](#main-documents)
- [Closure pending items](#closure-pending-items)

## Folder map

| Folder | Content | Status |
|---|---|---|
| [`schematics/`](schematics/) | Electrical schematics and visual exports. | In progress |
| [`wiring_diagrams/`](wiring_diagrams/) | Practical wiring documentation and connector tables. | Partial |
| [`pinout_tables/`](pinout_tables/) | ESP32, Raspberry Pi and CAN-module pinout tables. | Advanced |
| [`power_distribution/`](power_distribution/) | Power supply, 12 V actuator rail, 5 V logic rail and grounding notes. | Updated, pending measurements/photos |
| [`images/`](images/) | Electronics photos and captures. | Pending final photos |

## Current status

| Block | Status | Reference |
|---|---|---|
| ESP32 node pinout | Documented | [`pinout_tables/esp32_pinout_table.md`](pinout_tables/esp32_pinout_table.md) |
| Raspberry Pi + MCP2515 | Documented | [`pinout_tables/raspberry_pi_mcp2515.md`](pinout_tables/raspberry_pi_mcp2515.md) |
| Main bus | Documented in text | [`wiring_diagrams/bus_principal.md`](wiring_diagrams/bus_principal.md) |
| Controller nodes | Driver assignment documented, physical verification pending | [`wiring_diagrams/nodos_controladores.md`](wiring_diagrams/nodos_controladores.md) |
| Connector table | Template created, physical connector data pending | [`wiring_diagrams/connector_table.md`](wiring_diagrams/connector_table.md) |
| Power distribution | Updated with Dell 12 V supply, LM2596S 5 V converter and panic-button behavior | [`power_distribution/power_summary.md`](power_distribution/power_summary.md) |
| Schematics | Structure and review criteria ready | [`schematics/schematics_index.md`](schematics/schematics_index.md) |

## Main documents

- [`schematics/README.md`](schematics/README.md)
- [`schematics/schematics_index.md`](schematics/schematics_index.md)
- [`pinout_tables/esp32_pinout_table.md`](pinout_tables/esp32_pinout_table.md)
- [`pinout_tables/raspberry_pi_mcp2515.md`](pinout_tables/raspberry_pi_mcp2515.md)
- [`wiring_diagrams/bus_principal.md`](wiring_diagrams/bus_principal.md)
- [`wiring_diagrams/nodos_controladores.md`](wiring_diagrams/nodos_controladores.md)
- [`wiring_diagrams/connector_table.md`](wiring_diagrams/connector_table.md)
- [`power_distribution/power_summary.md`](power_distribution/power_summary.md)

## Closure pending items

- [ ] Confirm final schematic filenames and exports.
- [ ] Export each editable schematic to PDF/PNG.
- [ ] Add real electronics photos in [`images/`](images/).
- [ ] Fill final connector table from physical inspection.
- [ ] Confirm Dell server power-supply model.
- [ ] Measure 12 V actuator rail current during representative tests.
- [ ] Measure 5 V logic rail current.
- [ ] Verify consistency between schematics, connector table, pinouts, firmware and BOM.

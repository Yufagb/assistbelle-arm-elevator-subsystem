<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Raspberry Pi 5 to MCP2515

This document describes the Raspberry Pi 5 to MCP2515 CAN interface used in the Assistbelle robotic arm and elevator subsystem.

## Source

- Thesis / schematic reference: `RASPBERRYPI_MCP2515.pdf`.
- The reviewed schematic shows a Raspberry Pi 40-pin header, an MCP2515 10-pin header, a 2-pin CAN connector and a 2-pin power connector.

## Operating voltage note

The real implementation uses **5 V to power the MCP2515 module**.

The Raspberry Pi SPI and interrupt signals remain Raspberry Pi logic-level signals. Therefore, the MCP2515 module used in the final setup must be compatible with Raspberry Pi 3.3 V logic on the SPI/INT side, either through an appropriate module design, onboard level shifting or verified safe interface behavior.

## Pin mapping

| MCP2515 signal | Raspberry Pi BCM GPIO | Raspberry Pi physical pin | Notes |
|---|---:|---:|---|
| VCC / module power | - | 2 / 4 | 5 V supply for the MCP2515 module. |
| GND | - | 6 | Signal ground reference. |
| CS / CS_CAN | GPIO8 | 24 | SPI0 CE0, CAN interface chip select. |
| SCK | GPIO11 | 23 | SPI clock. |
| MOSI | GPIO10 | 19 | Data from Raspberry Pi to MCP2515. |
| MISO | GPIO9 | 21 | Data from MCP2515 to Raspberry Pi. |
| INT / INT_CAN | GPIO25 | 22 | MCP2515 interrupt line. |
| CANH | - | - | CAN high differential line. |
| CANL | - | - | CAN low differential line. |

## Schematic connector reference

| Connector | Pin count | Signals | Notes |
|---|---:|---|---|
| `J_RPI` | 40 | Raspberry Pi 40-pin GPIO header | Includes 3V3, 5V, GND, MOSI, MISO, SCK, CS_CAN and INT_CAN labels. |
| `J_MCP` | 10 | 3V3, GND, SCK, MOSI, MISO, CS_CAN, NC, INT_CAN, CANL, CANH | Header shown in the schematic for the MCP2515 module interface. |
| `J_CAN` | 2 | CANH, CANL | CAN bus connector. |
| `J_POWER` | 2 | 5V, GND | 5 V power connector used for the MCP2515 module supply in the real implementation. |

## Configuration used

```bash
dtparam=spi=on
dtoverlay=spi-bcm2835
dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=25
```

## CAN startup

```bash
sudo ip link set can0 down 2>/dev/null || true
sudo ip link set can0 up type can bitrate 500000
ip -details link show can0
```

## Quick checks

```bash
ls /dev/spidev*
lsmod | grep -i spi
lsmod | grep -E 'mcp251x|can'
sudo modprobe mcp251x
sudo modprobe can_raw
sudo modprobe can_dev
ip link show
candump can0
```

## Electrical notes

- MCP2515 module supply in the current implementation: **5 V**.
- Raspberry Pi SPI/INT logic compatibility must be preserved at **3.3 V logic level**.
- Use 120-ohm CAN termination only at the physical ends of the CAN bus.
- All CAN nodes must use the same bitrate.
- The documented CAN bitrate is **500 kbit/s**.
- Confirm physically that CANH and CANL are not swapped.

## Physical verification checklist

- [ ] Photograph Raspberry Pi 5 to MCP2515 wiring.
- [ ] Confirm the MCP2515 module receives 5 V at its power input.
- [ ] Confirm the specific MCP2515 module used is safe for Raspberry Pi 3.3 V SPI/INT logic.
- [ ] Confirm `CS_CAN` is connected to GPIO8 / physical pin 24.
- [ ] Confirm `INT_CAN` is connected to GPIO25 / physical pin 22.
- [ ] Confirm CANH/CANL orientation at `J_CAN`.
- [ ] Update `electronics/images/README.md` with the final photo name when uploaded.

## Related documents

- [`../schematics/RASPBERRYPI_MCP2515.pdf`](../schematics/RASPBERRYPI_MCP2515.pdf)
- [`../schematics/schematics_index.md`](../schematics/schematics_index.md)
- [`../wiring_diagrams/connector_table.md`](../wiring_diagrams/connector_table.md)
- [`../wiring_diagrams/bus_principal.md`](../wiring_diagrams/bus_principal.md)

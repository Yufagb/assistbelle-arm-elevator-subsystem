<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Bill of materials summary table

This table summarizes the current HardwareX elevator bill of materials (BOM) for manuscript use.

The complete machine-readable BOM is stored in:

```text
docs/bom/hardwarex_elevator_bom_final.csv
```

The GitHub-readable BOM is stored in:

```text
docs/bom/hardwarex_elevator_bom_final.md
```

## Current BOM snapshot

| Metric | Value |
|---|---:|
| BOM item rows | 32 |
| Estimated product/material total | USD 484.78 |
| Currency | USD estimates |
| Exchange-rate note | Local PEN prices converted at 1 USD = 3.3898 PEN where applicable |
| Cost coverage | Product/material cost only |
| Excluded costs | Shipping, customs, taxes and marketplace price changes |
| Source workbook | `ASM_Elevator_System_HardwareX_BOM` |
| Source tab | `BOM_Final_Clean` |
| Current uploaded CAD snapshot | v60 working snapshot |
| Raspberry Pi sourcing | Estimated cost; exact selected seller/product pending |

## Category summary

| Category | Number of items | Estimated subtotal |
|---|---:|---:|
| Structure | 6 | USD 122.14 |
| Actuation | 6 | USD 81.58 |
| Guiding | 3 | USD 78.30 |
| Fasteners | 13 | USD 37.51 |
| Electronics | 3 | USD 165.25 |
| **Total** | **32** | **USD 484.78** |

## Key installed components

| BOM ID | Component | Quantity | Category | Notes |
|---|---|---:|---|---|
| `BUY_STR_001` | V-Slot 20x40 vertical rail, 600 mm | 2 | Structure | Main vertical rail structure. |
| `BUY_STR_004` | V-Slot 20x40 top crossbar, 500 mm | 1 | Structure | Top crossbar. |
| `FAB_STR_001` | Base plate, 356 x 356 x 15 mm | 1 | Structure | MDF fabricated base plate. |
| `FAB_STR_002` | Top plate, 420 x 400 x 3 mm | 1 | Structure | Stainless-steel fabricated top plate. |
| `BUY_ACT_001` | NEMA 23 stepper motor JK57HS51-2804 | 2 | Actuation | Elevator motors. |
| `BUY_ACT_002` | TR8x8 lead screw, 550 mm | 2 | Actuation | Elevator screw drive. |
| `BUY_ACT_003` | Flexible coupler, 6.35 x 8 mm | 2 | Actuation | Motor-to-lead-screw coupling. |
| `BUY_ACT_005` | TR8 nut block housing | 2 | Actuation | Purchased nut block support. |
| `FAB_ACT_002` | NEMA 23 mounting plate | 2 | Actuation | ABS fabricated/printed mount. |
| `BUY_GUI_003` | V-wheel kit with bearings | 8 | Guiding | Dual V-wheel guiding hardware. |
| `FAB_GUI_001` | Gantry plate, 127 x 88 x 3 mm | 4 | Guiding | Stainless-steel fabricated gantry plate. |
| `FAB_GUI_002` | Spacer block | 4 | Guiding | ABS gray printed/fabricated spacer block. |
| `BUY_ELE_001` | Raspberry Pi 5, 8 GB RAM | 1 | Electronics | Main computer / ROS 2 side; exact seller pending. |
| `BUY_ELE_002` | MCP2515 CAN-SPI module | 1 | Electronics | Raspberry Pi CAN interface. |
| `BUY_ELE_003` | TB6600 stepper motor driver module | 2 | Electronics | Two drivers for the two J5/elevator NEMA 23 motors. |

## BOM notes for manuscript use

- The total is an estimated product/material cost only.
- Shipping, taxes, customs, tooling, consumables and marketplace price changes are excluded.
- Fabricated part costs are prototype estimates and should be rechecked before replication.
- Purchased subassemblies are counted at the procurement level to avoid double-counting internal CAD subparts.
- Legacy or removed components such as Astra/Astra Plus cameras, LiPo batteries, tablet and DRV8825 are excluded from the active elevator BOM.
- `FAB_GUI_001` was corrected from an older `20 x 80 mm` description to `127 x 88 x 3 mm` based on the current v60 CAD/drawing.
- Before final HardwareX submission, confirm the exact Raspberry Pi 5 supplier/product and freeze the final CAD/BOM release version.

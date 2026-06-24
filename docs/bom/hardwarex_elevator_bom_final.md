<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# HardwareX Elevator BOM

Readable bill of materials for the Assistbelle vertical elevator subsystem, prepared for the HardwareX publication package.

The complete machine-readable source table is available in [`hardwarex_elevator_bom_final.csv`](hardwarex_elevator_bom_final.csv). This Markdown file is a human-readable summary for GitHub navigation and reviewer readability.

## Snapshot

| Metric | Value |
|---|---:|
| BOM item rows | 29 |
| Estimated product total | USD 408.85 |
| Currency | USD estimates |
| Cost coverage | Product cost only |
| Excluded costs | Shipping, customs, taxes and marketplace price changes |
| Source workbook | `ASM_Elevator_System_HardwareX_BOM` |
| Source tab | `BOM_Final_Clean` |
| Source CAD release | `ASM_Elevator_System.step` + `ASM_Elevator_System.f3z`, v54 |
| Export date | 2026-06-23 |

## Category summary

| Category | Items | Estimated subtotal |
|---|---:|---:|
| Structure | 6 | USD 122.49 |
| Actuation | 6 | USD 139.34 |
| Guiding | 3 | USD 98.19 |
| Fasteners | 13 | USD 48.83 |
| **Total** | **29** | **USD 408.85** |

## Structure

| ID | Part | Type | Qty | Material | Supplier | Total |
|---|---|---|---:|---|---|---:|
| `BUY_STR_001` | V-Slot 20x40 vertical rail, 600 mm | Purchased | 2 pcs | Anodized aluminum | Naylamp Mechatronics | USD 24.84 |
| `BUY_STR_002` | V-Slot L bracket, 20 mm | Purchased | 24 pcs | Aluminum 6105-T5 | Naylamp Mechatronics | USD 23.42 |
| `BUY_STR_003` | V-Slot L bracket, 40 mm | Purchased | 10 pcs | Aluminum 6105-T5 | Naylamp Mechatronics | USD 13.60 |
| `BUY_STR_004` | V-Slot 20x40 top crossbar, 500 mm | Purchased | 1 pc | Anodized aluminum | Naylamp Mechatronics | USD 10.35 |
| `FAB_STR_001` | Base plate, 356 x 356 x 15 mm | Fabricated | 1 pc | MDF | Local fabrication | USD 5.92 |
| `FAB_STR_002` | Top plate, 420 x 400 x 3 mm | Fabricated | 1 pc | Stainless steel | Local fabrication | USD 44.36 |

## Actuation

| ID | Part | Type | Qty | Material | Supplier | Total |
|---|---|---|---:|---|---|---:|
| `BUY_ACT_001` | NEMA 23 stepper motor JK57HS51-2804 | Purchased | 2 pcs | Commercial motor | AliExpress | USD 80.00 |
| `BUY_ACT_002` | TR8x8 lead screw, 550 mm | Purchased | 2 pcs | Steel | AliExpress | USD 37.00 |
| `BUY_ACT_003` | Flexible coupler, 6.35 x 8 mm | Purchased | 2 pcs | Aluminum | Naylamp Mechatronics | USD 8.87 |
| `BUY_ACT_004` | T8 lead screw nut, lead 8 mm | Purchased | 2 pcs | Brass/metal | AliExpress | USD 4.00 |
| `BUY_ACT_005` | TR8 nut block housing | Purchased | 2 pcs | Delrin/metal | Naylamp Mechatronics | USD 6.51 |
| `FAB_ACT_002` | NEMA 23 mounting plate | Fabricated | 2 pcs | ABS | Local fabrication | USD 2.96 |

## Guiding

| ID | Part | Type | Qty | Material | Supplier | Total |
|---|---|---|---:|---|---|---:|
| `BUY_GUI_003` | V-wheel kit with bearings | Purchased | 8 pcs | Polycarbonate wheel + 625RS bearings | Naylamp Mechatronics | USD 33.12 |
| `FAB_GUI_001` | Gantry plate, 20 x 80 mm | Fabricated | 4 pcs | Stainless steel | Local fabrication | USD 59.15 |
| `FAB_GUI_002` | Spacer block | Fabricated | 4 pcs | ABS, gray | Local fabrication | USD 5.92 |

## Fasteners

| ID | Part | Type | Qty | Supplier | Total |
|---|---|---|---:|---|---:|
| `STD_FAS_001` | Screw, McMaster 90258A232 | Standard hardware | 12 pcs | McMaster-Carr | USD 24.00 |
| `STD_FAS_002` | Screw, McMaster 92125A192 | Standard hardware | 8 pcs | McMaster-Carr | USD 0.48 |
| `STD_FAS_003` | Hex nut, McMaster 90592A090 | Standard hardware | 8 pcs | McMaster-Carr | USD 0.16 |
| `STD_FAS_004` | Socket head screw, McMaster 92290A148 | Standard hardware | 8 pcs | McMaster-Carr | USD 6.40 |
| `STD_FAS_005` | Shim, McMaster 96945A303 | Standard hardware | 12 pcs | McMaster-Carr | USD 2.40 |
| `STD_FAS_006` | Hex nut, McMaster 90592A011 | Standard hardware | 50 pcs | McMaster-Carr | USD 1.00 |
| `STD_FAS_007` | Thread-forming screw, McMaster 99461A973 | Standard hardware | 10 pcs | McMaster-Carr | USD 0.80 |
| `STD_FAS_008` | M5 wheel spacer | Standard hardware | 16 pcs | Naylamp Mechatronics | USD 2.84 |
| `STD_FAS_009` | Truss head screw, McMaster 92467A517 | Standard hardware | 8 pcs | McMaster-Carr | USD 0.96 |
| `STD_FAS_010` | Flat head screw, McMaster 92125A208 | Standard hardware | 32 pcs | McMaster-Carr | USD 2.56 |
| `STD_FAS_011` | M5 T-slot nut for 2020 profile | Standard hardware | 32 pcs | Naylamp Mechatronics | USD 3.79 |
| `STD_FAS_012` | Pan head screw, McMaster 92000A220 | Standard hardware | 12 pcs | McMaster-Carr | USD 3.12 |
| `STD_FAS_013` | Thread-forming screw, McMaster 99461A971 | Standard hardware | 4 pcs | McMaster-Carr | USD 0.32 |

## Source and supplier notes

- Exact sourcing links and alternative/local supplier links are preserved in the CSV file.
- Purchased subassemblies are counted at the procurement level.
- Internal V-wheel CAD subparts are excluded to avoid double counting.
- McMaster-Carr part numbers are retained for CAD-coded standard fasteners.
- Fabricated part costs are prototype estimates and should be verified before final replication.

## Publication notes

Before final HardwareX submission:

- Confirm stock, shipping and pack sizes for all supplier links.
- Re-check CAD-derived fastener quantities, especially `STD_FAS_010` and `STD_FAS_011`.
- Keep private receipts, reimbursement files and raw order screenshots outside the public repository unless redacted.
- If the Google Sheet changes, re-export the CSV and regenerate this Markdown summary.

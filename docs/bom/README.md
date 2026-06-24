<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Bill of materials

This folder stores the curated bill of materials (BOM) files for the Assistbelle elevator/arm HardwareX package.

## Recommended reading order

1. Open [`hardwarex_elevator_bom_final.md`](hardwarex_elevator_bom_final.md) for the readable GitHub-rendered BOM.
2. Open [`hardwarex_elevator_bom_final.csv`](hardwarex_elevator_bom_final.csv) for the complete machine-readable/source table.
3. Use [`../bom_template.csv`](../bom_template.csv) only as the previous Spanish/PEN reference BOM.

## Files

| File | Purpose | Source | Status |
|---|---|---|---|
| [`hardwarex_elevator_bom_final.md`](hardwarex_elevator_bom_final.md) | Human-readable Markdown summary with category subtotals, compact tables and CAD naming guide. | Generated from `hardwarex_elevator_bom_final.csv`. | Current readable BOM for GitHub reviewers. |
| [`hardwarex_elevator_bom_final.csv`](hardwarex_elevator_bom_final.csv) | Final clean BOM export for the elevator CAD v54 review, synchronized with the Google Sheet. | Google Sheet `ASM_Elevator_System_HardwareX_BOM`, tab `BOM_Final_Clean`, spreadsheet ID `13egV0GarW81nshgVwWWbSk6_NnhDDFxmWRa8S5-cg0I`. | Current exported BOM snapshot. |
| [`../bom_template.csv`](../bom_template.csv) | Previous active public BOM template in Spanish/PEN format. | Earlier procurement reconciliation work. | Retained for continuity; superseded for the elevator-specific HardwareX BOM by `hardwarex_elevator_bom_final.csv`. |

## Source snapshot

| Field | Value |
|---|---|
| Source workbook title | `ASM_Elevator_System_HardwareX_BOM` |
| Source tab | `BOM_Final_Clean` |
| CAD inputs noted in source workbook | `ASM_Elevator_System.step` and `ASM_Elevator_System.f3z` |
| CAD release noted in source workbook | `v54` |
| Source-generated date | `2026-06-23` |
| Last repository BOM update | `2026-06-23` |
| BOM rows | 32 item rows + 1 estimated-total row |
| Estimated product/material total | USD 484.78 |
| Currency | USD estimates |
| Exchange-rate note | Local PEN prices converted at 1 USD = 3.3898 PEN where applicable |
| Cost coverage | Product/material cost only; shipping, customs, taxes and marketplace price changes excluded. |

## Counting rule

Purchased subassemblies are counted at the procurement level. Internal V-wheel CAD subparts are excluded to avoid double counting. This follows the note in the source workbook README tab.

## Supplier-reference rule

The current CSV keeps one `Purchase URL` column with the selected source for each item. Source handling follows these rules:

1. Prefer exact AliExpress product links when the exact purchased or equivalent product is identifiable.
2. Use Peru/local suppliers such as Naylamp when they are active and useful for replication.
3. Use McMaster-Carr direct links for CAD-coded standard fasteners.
4. For fabricated parts, include local material or fabrication-service references, then document actual prototype cost in the remarks.

## CAD naming rule

CAD browser/component names should start with the matching BOM item ID when possible. The current electronics additions use:

| BOM ID | CAD name pattern |
|---|---|
| `BUY_ELE_001` | `BUY_ELE_001_RaspberryPi5_8GB_SBC` |
| `BUY_ELE_002` | `BUY_ELE_002_MCP2515_CAN_SPI_Module` |
| `BUY_ELE_003` | `BUY_ELE_003_TB6600_Stepper_Driver_J5_MotorA` and `BUY_ELE_003_TB6600_Stepper_Driver_J5_MotorB` |

## Review notes before publication

- Confirm stock, pack size and shipping before purchasing; prices are references and may change.
- Review odd or CAD-derived quantities such as `STD_FAS_010` and `STD_FAS_011` against the final CAD assembly.
- Confirm whether the two TB6600 drivers correspond to left/right or Motor A/Motor B in the final wiring diagram.
- Replace the Raspberry Pi 5 estimate with an exact selected supplier link when available.
- Keep private raw receipts, reimbursement sheets and order screenshots out of the public repository unless they are redacted.
- If a row changes in the Google Sheet or CAD adds/removes components, re-export/update the CSV snapshot and regenerate the Markdown summary in the same commit.

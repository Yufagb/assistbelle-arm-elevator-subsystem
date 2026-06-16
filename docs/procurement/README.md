<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Procurement and purchase evidence

This folder organizes public procurement information for the Assistbelle robotic arm and elevator subsystem HardwareX package.

## Purpose

The files in this folder help trace purchased components, suppliers and approximate costs without exposing private financial documents, full order screenshots, card statements or personal account information in the public repository.

## Privacy and publication policy

The original evidence files uploaded for review include purchase/order exports, AliExpress order screenshots and UTEC expense-liquidation spreadsheets. These raw files may contain private order references, personal account information, reimbursement details or institutional financial data. For this public HardwareX repository, only a curated public summary is stored here.

Do **not** upload raw receipts, card statements, full order screenshots or reimbursement spreadsheets to this public repository unless they have been explicitly reviewed and redacted.

## Files

| File | Purpose | Status |
|---|---|---|
| [`purchase_log_public.csv`](purchase_log_public.csv) | Public, normalized purchase/procurement evidence log. | Created from uploaded purchase documents. |
| [`../bom_template.csv`](../bom_template.csv) | Active BOM for the HardwareX package. | Existing active BOM; must be reconciled against this procurement log. |

## Sources reviewed

| Uploaded source | Content extracted | Public handling |
|---|---|---|
| `Lista de Materiales (1).xlsx` | Initial material list with categories, systems, purchase status, costs, suppliers and links. | Used as background for BOM reconciliation; raw workbook not uploaded. |
| `Orders.pdf` | AliExpress completed orders from April and May 2025, including mechanical parts, electronics, bearings, DRV8871, DC-DC converter and legacy DRV8825 purchase. | Summarized into the public purchase log without exposing full raw order pages. |
| `2_Liquidación de gastos (2F) 31_03_2025.xlsx` | Expense-liquidation rows including TB6600/NEMA23, MCP2515, Micro DC Motors, mechanical materials and electronics. | Summarized into the public purchase log; raw reimbursement file not uploaded. |
| `2F Liquidacion tarjeta corporativa.xlsx` | Corporate-card liquidation rows including V-slot, fasteners, fabrication, ESP32 and legacy BTS7960 purchases. | Summarized into the public purchase log; raw reimbursement file not uploaded. |

## Current public purchase-log summary

| Metric | Value |
|---|---:|
| Public log rows | 39 |
| Total summarized amount | S/ 2,575.676 |
| Currency | PEN / Soles |
| Evidence period | April 2025 to December 2025 |
| Raw files uploaded to public repo | No |

## Active vs legacy handling

Some purchases were made during development but are not part of the current public HardwareX design. These are retained in the public log as historical evidence but should not be added to the active BOM unless the final design uses them.

| Item / family | Current handling |
|---|---|
| DRV8871 | Active for J1/J4 DC motor-driver documentation. |
| IBT-2 / BTS7960 | J2/J3 physical driver assignment must be verified; BTS7960 purchases are marked legacy/to-review unless confirmed in the final robot. |
| TB6600 + NEMA23 | Active for J5/elevator. |
| DRV8825 / A4988 / NEMA17 | Legacy or to-review; not part of current final elevator-driver choice. |
| MCP2515 | Active CAN master interface. |
| LM2596S 5 V converter | Active logic power supply. |
| V-slot profiles, brackets and fasteners | Active or to-reconcile with mechanical CAD and fastener table. |

## Reconciliation workflow

Before freezing the HardwareX BOM:

1. Compare each active purchase-log row with [`../bom_template.csv`](../bom_template.csv).
2. Split bundle purchases when needed, for example TB6600 + NEMA23 + ACS sensors.
3. Mark tools and consumables separately from installed components.
4. Keep legacy purchases in the procurement log but out of the active BOM.
5. Add exact quantities, final unit costs and final supplier alternatives.
6. Cross-check mechanical items against `hardware/fasteners/`, CAD and photos.
7. Cross-check electronics items against `electronics/schematics/`, `electronics/wiring_diagrams/connector_table.md` and photos.

## Pending information

- Exact Dell server PSU model.
- Final split of bundled purchases into individual BOM lines.
- Confirmation of which V-slot, bracket and fastener purchases are installed in the final prototype.
- Confirmation whether any BTS7960/IBT-2 purchase line corresponds to final J2/J3 hardware.
- Final supplier alternatives for components with one-off local purchases.
- Public photos/evidence in `electronics/images/` and `hardware/photos/`.

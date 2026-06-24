<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Procurement and purchase evidence

This folder organizes public procurement information for the Assistbelle robotic arm and elevator subsystem HardwareX package.

## Purpose

The files in this folder help trace purchased components, suppliers and approximate costs without exposing private financial documents, full order screenshots, card statements or personal account information in the public repository.

## Privacy and publication policy

The original evidence files uploaded for review include purchase/order exports, AliExpress order screenshots, UTEC expense-liquidation spreadsheets and project Google Sheets. These raw files may contain private order references, personal account information, reimbursement details or institutional financial data. For this public HardwareX repository, only curated public summaries are stored here.

Do **not** upload raw receipts, card statements, full order screenshots or reimbursement spreadsheets to this public repository unless they have been explicitly reviewed and redacted.

## Files

| File | Purpose | Status |
|---|---|---|
| [`purchase_log_public.csv`](purchase_log_public.csv) | Public, normalized purchase/procurement evidence log. | Created from uploaded purchase documents. |
| [`usage_reconciliation.md`](usage_reconciliation.md) | Active/legacy/to-reconcile classification from purchases, schematics, firmware, current docs and user build confirmations. | Updated; photos and exact placement evidence pending. |
| [`../../hardware/fasteners/structural_profiles_table.csv`](../../hardware/fasteners/structural_profiles_table.csv) | V-slot/profile/bracket/fastener reconciliation table. | Updated with user-confirmed active V-slot, brackets, Dual V wheels and threaded rod. |
| [`../bom_template.csv`](../bom_template.csv) | Earlier active public BOM in Spanish/PEN format. | Retained for continuity; use the new HardwareX elevator BOM for the v54 elevator package. |
| [`../bom/hardwarex_elevator_bom_final.csv`](../bom/hardwarex_elevator_bom_final.csv) | Clean HardwareX elevator BOM exported from the project Google Sheet. | Current v54 BOM snapshot, sourced from `ASM_Elevator_System_HardwareX_BOM` / `BOM_Final_Clean`. |
| [`../bom/README.md`](../bom/README.md) | BOM source, counting rules and export traceability. | Current. |

## Sources reviewed

| Uploaded/source item | Content extracted | Public handling |
|---|---|---|
| `ASM_Elevator_System_HardwareX_BOM` Google Sheet | Final clean v54 elevator BOM with item IDs, categories, quantities, materials, processes, suppliers, URLs and USD cost estimates. | Exported as `docs/bom/hardwarex_elevator_bom_final.csv`; raw spreadsheet is not committed. |
| `Lista de Materiales (1).xlsx` | Initial material list with categories, systems, purchase status, costs, suppliers and links. | Used as background for BOM reconciliation; raw workbook not uploaded. |
| `Orders.pdf` | AliExpress completed orders from April and May 2025, including mechanical parts, electronics, bearings, DRV8871, DC-DC converter and legacy DRV8825 purchase. | Summarized into the public purchase log without exposing full raw order pages. |
| `2_Liquidación de gastos (2F) 31_03_2025.xlsx` | Expense-liquidation rows including TB6600/NEMA23, MCP2515, Micro DC Motors, mechanical materials and electronics. | Summarized into the public purchase log; raw reimbursement file not uploaded. |
| `2F Liquidacion tarjeta corporativa.xlsx` | Corporate-card liquidation rows including V-slot, fasteners, fabrication, ESP32 and BTS7960 purchases. | Summarized into the public purchase log; raw reimbursement file not uploaded. |
| Firmware and electronics docs | TB6600 code/pin evidence, controller-node assignments and schematic coverage. | Used to classify active vs legacy purchases. |
| User build confirmation during project review | Confirms both V-slot families, Dual V wheels, brackets, threaded rod and J2/J3 IBT-2 use. | Reflected in reconciliation docs; final photos/placement evidence still pending. |

## Current public purchase-log summary

| Metric | Value |
|---|---:|
| Public log rows | 39 |
| Total summarized amount | S/ 2,575.676 |
| Currency | PEN / Soles |
| Evidence period | April 2025 to December 2025 |
| Raw files uploaded to public repo | No |

## Current HardwareX BOM snapshot

| Metric | Value |
|---|---:|
| Source workbook | `ASM_Elevator_System_HardwareX_BOM` |
| Source tab | `BOM_Final_Clean` |
| CAD release noted by workbook | `v54` |
| Exported BOM rows | 29 item rows + 1 estimated-total row |
| Estimated product total | USD 408.85 |
| Cost exclusions | Shipping, customs, taxes and marketplace price changes |

## Active vs legacy handling

Some purchases were made during development but are not part of the current public HardwareX design. These are retained in the public log as historical evidence but should not be added to the active BOM unless the final design uses them.

| Item / family | Current handling |
|---|---|
| DRV8871 | Active for J1/J4 DC motor-driver documentation; final board/wiring photos pending. |
| IBT-2 / BTS7960 | User-confirmed active for J2/J3; excess BTS7960 purchases remain legacy unless physically installed. |
| TB6600 + NEMA23 | Active for J5/elevator; supported by BOM, procurement log and firmware/code documentation. |
| DRV8825 / A4988 / NEMA17 | Legacy or test/prototype only; not part of current final elevator-driver choice. |
| MCP2515 | Active CAN master interface. |
| LM2596S 5 V converter | Active logic power supply. |
| V-slot profiles, brackets and fasteners | User-confirmed active; final CAD/photo placement evidence pending. |

## Reconciliation workflow

Before freezing the HardwareX BOM:

1. Compare each active purchase-log row with [`../bom/hardwarex_elevator_bom_final.csv`](../bom/hardwarex_elevator_bom_final.csv).
2. Keep the previous [`../bom_template.csv`](../bom_template.csv) only as a continuity/reference file unless it is intentionally migrated to the new HardwareX format.
3. Split bundle purchases when needed, for example TB6600 + NEMA23 + ACS sensors.
4. Mark tools and consumables separately from installed components.
5. Keep legacy purchases in the procurement log but out of the active BOM.
6. Add exact quantities, final unit costs and final supplier alternatives.
7. Cross-check mechanical items against `hardware/fasteners/`, CAD and photos.
8. Cross-check electronics items against `electronics/schematics/`, `electronics/wiring_diagrams/connector_table.md` and photos.

## Pending information

- Exact Dell server PSU model.
- Final split of bundled purchases into individual BOM lines when more precision is required.
- Photo/placement evidence for V-slot 2040, V-slot 2020, brackets, Dual V wheels and threaded rod.
- Photo evidence and final pin mapping for J2/J3 IBT-2 modules.
- Public photos/evidence in `electronics/images/` and `hardware/photos/`.
- Re-export `docs/bom/hardwarex_elevator_bom_final.csv` whenever the Google Sheet source changes.

<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Fasteners and standard structural parts

This folder documents screws, nuts, bearings, rods, V-slot profiles, brackets, couplings and other standard mechanical parts used or purchased for the Assistbelle robotic arm and elevator subsystem.

## Files

| File | Purpose | Status |
|---|---|---|
| [`structural_profiles_table.csv`](structural_profiles_table.csv) | Reconciliation table for V-slot profiles, V-slot brackets, wheel kits, KP-08/KFL08 supports and related structural purchases. | Created from BOM and procurement evidence; physical verification pending. |
| `fasteners_table.csv` | Final installed screws, nuts, washers and small fasteners. | Pending. |
| `bearings_table.csv` | Final installed bearings and supports. | Pending. |

## Current V-slot / structural evidence summary

The current evidence has one important mismatch that must be resolved before freezing the HardwareX BOM:

| Evidence | Profile information | Status |
|---|---|---|
| Active BOM line `BOM-036` | `Perfil V-Slot 2040`, total 170 cm, described as 60 cm + 60 cm + 50 cm. | Active BOM baseline; verify on robot/CAD. |
| Procurement line `PRC-030` | `Perfil V-Slot 2020`, 70 cm x4 and 35 cm x2, total 350 cm. | Purchased structural material; reconcile before final BOM. |

Do not overwrite the active BOM quantity until the physical prototype and CAD confirm which profile family and lengths are installed.

## Physical verification needed

- [ ] Confirm whether the final frame uses V-Slot 2040, V-Slot 2020, or both.
- [ ] Measure final installed profile lengths.
- [ ] Photograph the installed V-slot profiles.
- [ ] Confirm installed quantity of 90-degree brackets and double L brackets.
- [ ] Confirm installed quantity of M5 screws and 2020 T-nuts.
- [ ] Confirm whether the 6 mm belt/NEMA17/A4988 kit was only for testing or belongs to another subsystem.
- [ ] Update `fasteners_table.csv` and `bearings_table.csv` after inspection.

## Related documents

- [`../../docs/bom_template.csv`](../../docs/bom_template.csv)
- [`../../docs/procurement/purchase_log_public.csv`](../../docs/procurement/purchase_log_public.csv)
- [`../../docs/procurement/usage_reconciliation.md`](../../docs/procurement/usage_reconciliation.md)

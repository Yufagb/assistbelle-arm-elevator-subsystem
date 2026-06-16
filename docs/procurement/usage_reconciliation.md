<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Procurement usage reconciliation

This document reconciles the purchase evidence, schematic PDFs, firmware/code references and current repository documentation to decide which purchased items are part of the current HardwareX arm/elevator package, which are legacy, and which still need physical confirmation.

## Evidence reviewed

| Evidence source | Use in this reconciliation |
|---|---|
| `docs/bom_template.csv` | Current active BOM baseline. |
| `docs/procurement/purchase_log_public.csv` | Curated public purchase/procurement log. |
| `electronics/schematics/*.pdf` | Electrical design evidence for active electronics blocks. |
| `firmware/esp32_stepper_node/J5_tb6600/` | Code-level evidence for the TB6600 elevator node. |
| `electronics/wiring_diagrams/nodos_controladores.md` | Current documented joint-to-driver assignment. |
| Uploaded expense/liquidation spreadsheets | Source of detailed purchase rows, summarized publicly in `purchase_log_public.csv`. |

## Usage categories

| Category | Meaning |
|---|---|
| Active | Used by the current HardwareX design or strongly supported by code/schematics/current docs. |
| Active / physical verification pending | Current documentation says it is used, but tomorrow's robot inspection/photos must confirm. |
| To reconcile | Purchased and probably relevant, but quantity, exact use or BOM mapping must be checked. |
| Legacy / not active | Purchased during development but not part of the current public HardwareX configuration. |
| Tool / consumable | Useful for fabrication/testing but not an installed robot component. |

## Electronics and actuator reconciliation

| Item family | Evidence | Decision | Notes |
|---|---|---|---|
| TB6600 drivers | BOM-038; purchase rows PRC-021/PRC-026; J5 firmware folder and code use TB6600 pins ENA/DIR/PUL. | Active | Final elevator driver family. |
| NEMA23 stepper motors | BOM-034; purchase rows PRC-021/PRC-026; J5 elevator subsystem documentation. | Active | Final elevator actuator family; exact installed motor count/photo still pending. |
| DRV8871 | BOM-014; purchase row PRC-015; DRV8871 schematic; node assignment J1/J4. | Active / physical verification pending | Current docs assign DRV8871 to J1 and J4. |
| IBT-2 / BTS7960 | Purchase rows PRC-018/PRC-035/PRC-038; IBT-2 schematic; node assignment J2/J3. | Active / physical verification pending for J2/J3; excess BTS7960 purchases legacy unless installed | Current docs assign IBT-2 to J2/J3, but physical driver boards must be photographed. |
| DRV8825 / A4988 / NEMA17 | Purchase rows PRC-009 and PRC-032. | Legacy / not active unless a test fixture is documented separately | Current J5 code and docs use TB6600 + NEMA23, not DRV8825/A4988/NEMA17. |
| MCP2515 | Purchase rows PRC-027/PRC-028; Raspberry Pi/MCP2515 schematic and pinout docs. | Active | Current implementation uses 5 V module power with Raspberry Pi 3.3 V SPI/INT compatibility to verify. |
| SN65HVD230 CAN transceivers | BOM-017; schematics for ESP32 nodes. | Active | Used for ESP32 CAN physical layer. |
| LM2596S 5 V converter | BOM-020; purchase row PRC-008; power docs. | Active | Logic 5 V rail. |
| ACS712 current sensors | BOM-005; purchase rows PRC-005/PRC-026. | Active / to place in final wiring | Used for current sensing; exact final placement/photo pending. |

## Mechanical and V-slot reconciliation

The purchase evidence includes two different V-slot/profile families that must be separated:

1. The current BOM has `Perfil V-Slot 2040` with a total length of 170 cm, described as 60 cm + 60 cm + 50 cm for the elevator frame.
2. The corporate-card liquidation purchase log includes `V-Slot 2020 profiles 70cm x4 and 35cm x2`, totaling 350 cm.

These are not the same profile/quantity, so the active BOM must not be overwritten until the physical frame/CAD confirms which profile family is installed.

| Item family | Evidence | Decision | Notes |
|---|---|---|---|
| V-Slot 2040, 170 cm | BOM-036. | Active BOM baseline / verify against robot | Current BOM says 2040 profile, 60+60+50 cm. |
| V-Slot 2020, 70 cm x4 + 35 cm x2 | PRC-030. | To reconcile / likely structural material | Purchase evidence says 2020 profile; verify if installed in final arm/elevator or used in prototype/testing. |
| Dual V wheel kit | BOM-035; PRC-013. | Active / reconcile cost | Used for V-slot guide system; photo/CAD placement pending. |
| V-2040 wheel/frame kit | BOM-037. | Active as reference/printed model candidate | BOM notes it was delivered and used as a reference for 3D-printed model. |
| KP-08 bearing blocks | PRC-031; T8/KP08 purchase evidence. | Active / fastener table pending | Likely part of lead-screw/elevator support; exact placement pending. |
| KFL08 / T8 screw support | PRC-003/PRC-010; BOM-033. | Active / reconcile duplicate purchases | Both KFL08 and KP08/T8 evidence exist; final quantity to verify. |
| V-slot 90-degree brackets | PRC-023/PRC-031/PRC-033. | Active / fastener table pending | Purchased in multiple rows; final installed quantity pending. |
| Universal double L brackets | PRC-033. | Active / fastener table pending | Needs physical/CAD placement. |
| M5 screws and T-nuts | PRC-031. | Active / fastener table pending | Likely used with V-slot system; final installed count pending. |
| Threaded rod 3/16 and hex nuts | PRC-034. | To reconcile / fastener table pending | Confirm if used in final prototype or only fabrication/testing. |
| Melamine/PVC/screws/adhesives | PRC-019/PRC-025. | Tooling/prototype support unless installed | Do not include as installed BOM unless final robot uses it. |

## Final status by purchase line groups

| Purchase line(s) | Item summary | Status for HardwareX |
|---|---|---|
| PRC-001 to PRC-006 | Worm gear, couplings, T8/KFL08, bearings, ACS712, stainless rod. | Mostly active/to-reconcile against mechanical CAD and BOM. |
| PRC-007 to PRC-008 | ESP32 and LM2596S. | Active. |
| PRC-009 | DRV8825. | Legacy/not active. |
| PRC-010 to PRC-015 | T8/KP08, bearings, wheels, PC817, DRV8871. | Active/to-reconcile. |
| PRC-016 to PRC-020 | Tape, cable ties, CNY70/BTS7960, consumables, hand saw. | Mixed: consumables/tooling; BTS7960 to verify only if used on J2/J3. |
| PRC-021 and PRC-026 | TB6600, NEMA23, ACS sensors. | Active, but bundled purchases should be split later. |
| PRC-027 to PRC-028 | MCP2515. | Active. |
| PRC-029 | Micro DC motors. | Active arm actuator evidence. |
| PRC-030 to PRC-034 | V-slot profiles, KP-08, brackets, fasteners, belt/V-slot kit, threaded rod. | Active/to-reconcile with CAD and physical build. |
| PRC-035 and PRC-038 | BTS7960 purchases. | Legacy unless physically confirmed as final J2/J3 IBT-2 implementation. |
| PRC-036 | Metal part fabrication. | Active/to-classify; identify part and drawing. |
| PRC-037 | ESP32/electronic circuit board. | Active/to-reconcile with ESP32 BOM quantity. |
| PRC-039 | Audio interface. | Out of current arm/elevator HardwareX scope unless later justified. |

## Actions before freezing the BOM

- [ ] Photograph J2 and J3 driver boards to confirm whether the installed module is IBT-2/BTS7960 and whether PRC-018/PRC-035/PRC-038 should be marked active or legacy.
- [ ] Compare the physical frame/CAD against V-Slot 2040 170 cm and V-Slot 2020 70 cm x4 + 35 cm x2.
- [ ] Create or complete `hardware/fasteners/structural_profiles_table.csv` with installed V-slot/profile/bracket/fastener quantities.
- [ ] Split bundle purchases PRC-021 and PRC-026 into TB6600, NEMA23 and ACS712 lines if final accounting precision is required.
- [ ] Mark DRV8825/A4988/NEMA17 as legacy unless a separate test fixture is documented.
- [ ] Identify the fabricated metal part from PRC-036 and connect it to CAD/drawings/photos.

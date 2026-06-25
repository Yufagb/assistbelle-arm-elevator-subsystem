<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Publication checklist for HardwareX

This checklist replaces the previous temporary checklist. It tracks the remaining work for submitting `assistbelle-arm-elevator-subsystem` as a public HardwareX-style open-source hardware package.

Legend:

- `[x]` done
- `[~]` partial
- `[ ]` pending
- `[d]` deferred / blocked by unavailable physical prototype or final release freeze

## 1. Repository organization

- [x] Public repository created: `Yufagb/assistbelle-arm-elevator-subsystem`.
- [x] Main branch selected for publication: `main`.
- [x] Root README reorganized for HardwareX.
- [x] Folder structure created: `docs/`, `electronics/`, `firmware/`, `hardware/`, `paper/`, `ros2_ws/`, `software/`, `validation/`.
- [x] `.gitignore` reinforced for ROS 2, Python, ESP-IDF, build folders and IDE folders.
- [x] Git LFS configured for large CAD, STEP, STL, DXF and media assets.
- [ ] Confirm there are no tracked generated files: `build/`, `install/`, `log/`, `.idea/`, `.vscode/`.

## 2. Licensing and citation

- [x] Root `LICENSE` file converted into a multi-license overview.
- [x] `LICENSES/Apache-2.0.txt` added for software, firmware and scripts.
- [x] `LICENSES/CERN-OHL-S-2.0.txt` added for hardware design files.
- [x] `LICENSES/CC-BY-4.0.txt` added for documentation and paper assets.
- [x] `CITATION.cff` added and updated to the public repository URL.
- [x] `docs/license_overview.md` updated with the license policy.
- [~] SPDX policy documented. Add file-level SPDX comments progressively when touching files.

## 3. Mechanical hardware

- [x] Upload editable CAD files: `hardware/cad/complete_robot/ASM_Elevator_System_v60.f3z`.
- [x] Upload full STEP export: `hardware/step/ASM_Elevator_System_v60.step`.
- [x] Upload STL exports for printable/fabricated parts currently identified in the elevator BOM.
- [x] Upload drawings with dimensions for fabricated plates.
- [x] Upload DXF fabrication files for stainless-steel cut plates.
- [~] Complete fasteners table: screws, nuts, bearings, profiles and standard parts are represented in BOM/fastener docs; final physical cross-check remains pending.
- [x] Confirm mechanical files are covered by CERN-OHL-S v2.0 through repository license policy.
- [d] Add photos of the assembled elevator/mechanical subsystem once the physical robot is accessible again.
- [d] STEP exports by subsystem are optional for the current v60 working snapshot and can be added before final release freeze.

## 4. Electronics

- [x] Pinout table for ESP32 nodes documented.
- [x] Raspberry Pi + MCP2515 documented.
- [x] Main CAN/power bus documented in text.
- [x] Schematics folder and index created.
- [~] Connector table updated with confirmed design intent; exact pin order, wire colors and connector models remain pending physical inspection.
- [~] Power summary updated with emergency-stop behavior and J5 dual-TB6600 notes; TB6600 supply voltage remains pending physical inspection.
- [ ] Confirm final schematic file names.
- [ ] Add final CAN diagram.
- [ ] Add final power-distribution diagram.
- [ ] Add electronics photos.
- [ ] Confirm electronics design files are covered by CERN-OHL-S v2.0.

## 5. Firmware

- [x] ESP32 firmware migrated to `firmware/`.
- [x] Firmware separated by node J1-J5.
- [x] ESP-IDF build guide added.
- [x] CAN IDs documented.
- [x] J5/TB6600 firmware included.
- [~] CAN payloads reviewed against ROS 2. `C5` is compatible; `B5` needs final decision because ROS expects position+velocity and current firmware returns position+reserved/status bytes.
- [ ] Document final safety limits in firmware.
- [ ] Decide final `B5` format and update firmware or ROS 2 accordingly.
- [ ] Add SPDX comments to source files when editing them.

## 6. ROS 2 software

- [x] Workspace kept in `ros2_ws/`.
- [x] `can_comm_pkg` included.
- [x] `can_node` validated with virtual CAN.
- [x] Main entry points documented.
- [~] J5 ROS/CAN compatibility documented; `C5` uses mm as `float32` little-endian.
- [ ] Validate all entry points one by one from a clean clone.
- [ ] Clarify whether product-identification scripts are ROS nodes or standalone helpers.
- [ ] Verify Python dependencies and system dependencies.
- [ ] Add SPDX comments to source files when editing them.

## 7. BOM

- [x] Clean HardwareX elevator BOM exported to `docs/bom/hardwarex_elevator_bom_final.csv`.
- [x] Human-readable BOM summary created at `docs/bom/hardwarex_elevator_bom_final.md`.
- [x] BOM synchronized with the current CAD/BOM review: 32 item rows + one estimated-total row.
- [x] Current estimated product/material total documented: USD 484.78.
- [x] Removed unused/legacy components from the active BOM scope: Astra/Astra Plus, LiPo, tablet and DRV8825.
- [x] DRV8871, IBT-2/BTS7960 and TB6600 differentiated in procurement and electronics documentation.
- [x] `FAB_GUI_001` updated to `Gantry plate, 127 x 88 x 3 mm` based on v60 CAD/drawing.
- [~] Separate installed components from tools/lab equipment if required by HardwareX.
- [~] Confirm final suppliers and alternatives; Raspberry Pi 5 exact seller/product remains pending.
- [~] Confirm final quantities after final CAD/mechanical freeze.

## 8. Manuals

- [x] Operation manual created.
- [x] Troubleshooting guide created.
- [x] Safety notes created.
- [~] Calibration manual created but still basic.
- [ ] Expand calibration with offsets, limits and direction checks.
- [ ] Expand safety notes with formal risk categories and pre-operation checklist.
- [ ] Add assembly instructions after CAD/mechanical closure.

## 9. Validation

- [x] Validation structure created.
- [x] Validation plan created.
- [x] Media index created.
- [x] Initial J5 motion summary created.
- [ ] Curate videos into `validation/media/` or provide stable external links.
- [ ] Curate final CSV files.
- [ ] Generate final figures.
- [ ] Document physical CAN validation.
- [ ] Document pick-and-place validation.
- [ ] Document perception validation.

## 10. Manuscript material

- [ ] Create manuscript draft or outline.
- [ ] Add final architecture figure.
- [ ] Add final electronics figure.
- [ ] Add final mechanical figure.
- [ ] Add validation figures and tables.
- [x] Add design-files summary table: `paper/tables/design_files_summary.md`.
- [x] Add BOM summary table: `paper/tables/bom_summary.md`.
- [ ] Add data availability statement.
- [ ] Add references.

## 11. Final cleanup

- [ ] Replace remaining placeholders.
- [ ] Check all links in root README and docs README.
- [ ] Confirm public access to repository.
- [ ] Confirm license policy is reflected in README, LICENSE and docs/license_overview.md.
- [ ] Run a clean-clone reproducibility test.
- [ ] Archive or remove obsolete temporary notes after final submission.

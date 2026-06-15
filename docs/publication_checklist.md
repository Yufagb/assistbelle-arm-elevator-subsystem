<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Publication checklist for HardwareX

This checklist replaces the previous temporary checklist. It tracks the remaining work for submitting `assistbelle-arm-elevator-subsystem` as a public HardwareX-style open-source hardware package.

Legend:

- `[x]` done
- `[~]` partial
- `[ ]` pending

## 1. Repository organization

- [x] Public repository created: `Yufagb/assistbelle-arm-elevator-subsystem`.
- [x] Main branch selected for publication: `main`.
- [x] Root README reorganized for HardwareX.
- [x] Folder structure created: `docs/`, `electronics/`, `firmware/`, `hardware/`, `paper/`, `ros2_ws/`, `software/`, `validation/`.
- [x] `.gitignore` reinforced for ROS 2, Python, ESP-IDF, build folders and IDE folders.
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

- [ ] Upload editable CAD files.
- [ ] Upload STEP exports.
- [ ] Upload STL exports for printable parts.
- [ ] Upload drawings with dimensions.
- [ ] Add photos of the assembled arm, elevator and gripper.
- [ ] Complete fasteners table: screws, nuts, bearings, profiles and standard parts.
- [ ] Confirm mechanical files are covered by CERN-OHL-S v2.0.

## 4. Electronics

- [x] Pinout table for ESP32 nodes documented.
- [x] Raspberry Pi + MCP2515 documented.
- [x] Main CAN/power bus documented in text.
- [x] Schematics folder and index created.
- [ ] Confirm final schematic file names.
- [ ] Add or export schematic PDFs/PNGs if only editable files exist.
- [ ] Add final CAN diagram.
- [ ] Add final power-distribution diagram.
- [ ] Add final connector table.
- [ ] Add electronics photos.
- [ ] Confirm electronics design files are covered by CERN-OHL-S v2.0.

## 5. Firmware

- [x] ESP32 firmware migrated to `firmware/`.
- [x] Firmware separated by node J1-J5.
- [x] ESP-IDF build guide added.
- [x] CAN IDs documented.
- [x] J5/TB6600 firmware included.
- [ ] Document final safety limits in firmware.
- [ ] Confirm CAN payloads match ROS 2 implementation.
- [ ] Add SPDX comments to source files when editing them.

## 6. ROS 2 software

- [x] Workspace kept in `ros2_ws/`.
- [x] `can_comm_pkg` included.
- [x] `can_node` validated with virtual CAN.
- [x] Main entry points documented.
- [ ] Validate all entry points one by one from a clean clone.
- [ ] Clarify whether product-identification scripts are ROS nodes or standalone helpers.
- [ ] Verify Python dependencies and system dependencies.
- [ ] Add SPDX comments to source files when editing them.

## 7. BOM

- [x] BOM CSV created at `docs/bom_template.csv`.
- [x] Removed unused components: Astra/Astra Plus, LiPo, tablet and DRV8825.
- [x] DRV8871 and TB6600 differentiated.
- [x] Current preliminary total documented: S/ 4,328.63.
- [ ] Separate installed components from tools/lab equipment if required by HardwareX.
- [ ] Confirm final suppliers and alternatives.
- [ ] Confirm final quantities after CAD/mechanical closure.

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
- [ ] Add design-files summary table.
- [ ] Add BOM summary table.
- [ ] Add data availability statement.
- [ ] Add references.

## 11. Final cleanup

- [ ] Replace remaining placeholders.
- [ ] Check all links in root README and docs README.
- [ ] Confirm public access to repository.
- [ ] Confirm license policy is reflected in README, LICENSE and docs/license_overview.md.
- [ ] Run a clean-clone reproducibility test.
- [ ] Archive or remove obsolete temporary notes after final submission.

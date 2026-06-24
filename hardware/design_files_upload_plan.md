<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Mechanical design files upload plan

This checklist defines the upload order, file names and target folders for the mechanical design package of the Assistbelle elevator subsystem.

Use this file to upload the HardwareX mechanical package step by step. The goal is to keep Fusion 360 editable files, neutral CAD exports, printable files, drawings and photos traceable to the BOM and CAD release v54.

## General rules

- Use version suffix `_v54` for files derived from the current CAD/BOM release.
- Use clear English file names for public HardwareX readability.
- Keep purchased commercial parts in the CAD/STEP assembly, but do not export every screw/nut as an individual file unless needed for reproduction.
- Upload STL files only for fabricated/3D-printed parts.
- Upload drawings/PDF/DXF only for fabricated or cut parts.
- Keep photos in `hardware/photos/`, not mixed with CAD files.
- Keep electronics photos in `electronics/images/`, not in `hardware/photos/`.

## Step 1 — Editable Fusion 360 assembly

| Status | Source file to upload | Target path | Required? | Notes |
|---|---|---|---|---|
| [ ] | `ASM_Elevator_System.f3z` | `hardware/cad/complete_robot/ASM_Elevator_System_v54.f3z` | Yes | Preferred editable assembly export because `.f3z` preserves referenced components. |
| [ ] | `ASM_Elevator_System.f3d` | `hardware/cad/complete_robot/ASM_Elevator_System_v54.f3d` | Optional | Upload only if it is a standalone Fusion design and does not depend on external references. |

## Step 2 — Full neutral CAD export

| Status | Source file to upload | Target path | Required? | Notes |
|---|---|---|---|---|
| [ ] | `ASM_Elevator_System.step` | `hardware/step/ASM_Elevator_System_v54.step` | Yes | Main neutral CAD file for reviewers who do not use Fusion 360. |

## Step 3 — STEP exports by subsystem

| Status | Source/export name | Target path | Required? | Notes |
|---|---|---|---|---|
| [ ] | Frame subsystem STEP | `hardware/step/ASM_Elevator_Frame_v54.step` | Recommended | V-slot frame, base/top plates and structural brackets. |
| [ ] | Carriage subsystem STEP | `hardware/step/ASM_Elevator_Carriage_v54.step` | Recommended | Moving carriage, gantry plates, spacers and V-wheel assemblies. |
| [ ] | Drive subsystem STEP | `hardware/step/ASM_Elevator_Drive_TR8_NEMA23_v54.step` | Recommended | NEMA23 motors, couplers, lead screws, nut blocks and supports. |
| [ ] | Guide subsystem STEP | `hardware/step/ASM_Elevator_Guide_VWheels_v54.step` | Recommended | Dual V-wheel guide path and wheel assemblies. |
| [ ] | Electronics mounting STEP | `hardware/step/ASM_Elevator_Electronics_Mounting_v54.step` | Optional | Raspberry Pi, MCP2515 and TB6600 placement if electronics mounting is part of the CAD. |

## Step 4 — STL files for 3D-printed/custom printed parts

| Status | BOM ID | Source/export name | Target path | Required? |
|---|---|---|---|---|
| [ ] | `FAB_ACT_002` | NEMA 23 mounting plate STL | `hardware/stl/FAB_ACT_002_NEMA23_Mounting_Plate_ABS_v54.stl` | Yes, if printed |
| [ ] | `FAB_GUI_002` | Spacer block STL | `hardware/stl/FAB_GUI_002_Spacer_Block_ABS_Gray_v54.stl` | Yes, if printed |
| [ ] | TBD | Any additional printed mount/bracket | `hardware/stl/<BOM_ID>_<Part_Name>_v54.stl` | If applicable |

Do not upload STL exports of purchased items such as V-slot profiles, NEMA23 motors, TB6600 drivers, Raspberry Pi, MCP2515 modules, screws, bearings or wheels unless the STL is needed as a visual placeholder only.

## Step 5 — Fabrication drawings and DXF files

| Status | BOM ID | Drawing/export name | Target path | Required? |
|---|---|---|---|---|
| [ ] | `FAB_STR_001` | MDF base plate drawing | `hardware/drawings/FAB_STR_001_Base_Plate_356x356x15_MDF_v54.pdf` | Yes |
| [ ] | `FAB_STR_002` | Stainless steel top plate drawing | `hardware/drawings/FAB_STR_002_Top_Plate_420x400x3_StainlessSteel_v54.pdf` | Yes |
| [ ] | `FAB_GUI_001` | Stainless steel gantry plate drawing | `hardware/drawings/FAB_GUI_001_Gantry_Plate_20x80_StainlessSteel_v54.pdf` | Yes |
| [ ] | `FAB_STR_002` | Top plate DXF | `hardware/drawings/FAB_STR_002_Top_Plate_420x400x3_StainlessSteel_v54.dxf` | Recommended if laser/waterjet cut |
| [ ] | `FAB_GUI_001` | Gantry plate DXF | `hardware/drawings/FAB_GUI_001_Gantry_Plate_20x80_StainlessSteel_v54.dxf` | Recommended if laser/waterjet cut |

## Step 6 — Mechanical photos

| Status | Photo to upload | Target path | Required? | Notes |
|---|---|---|---|---|
| [ ] | Full elevator front view | `hardware/photos/IMG_Elevator_Assembled_Front_v54.jpg` | Yes | Overall view for publication. |
| [ ] | Full elevator side view | `hardware/photos/IMG_Elevator_Assembled_Side_v54.jpg` | Yes | Shows depth, guide layout and frame. |
| [ ] | Carriage and V-wheel close-up | `hardware/photos/IMG_Elevator_Carriage_VWheels_v54.jpg` | Yes | Confirms Dual V-wheel guide implementation. |
| [ ] | TR8/NEMA23 drive close-up | `hardware/photos/IMG_Elevator_TR8_NEMA23_Drive_v54.jpg` | Yes | Confirms lead screw, coupler and motor placement. |
| [ ] | Top plate close-up | `hardware/photos/IMG_Elevator_Top_Plate_v54.jpg` | Recommended | Shows upper structure and supports. |
| [ ] | Base plate close-up | `hardware/photos/IMG_Elevator_Base_Plate_v54.jpg` | Recommended | Shows base structure, brackets and electronics placement if visible. |

## Step 7 — Electronics photos, stored separately

Electronics photos belong in `electronics/images/`.

| Status | Photo to upload | Target path | Required? |
|---|---|---|---|
| [ ] | Raspberry Pi + MCP2515 close-up | `electronics/images/IMG_RaspberryPi5_MCP2515_v54.jpg` | Yes |
| [ ] | TB6600 driver A close-up | `electronics/images/IMG_TB6600_Driver_J5_MotorA_v54.jpg` | Yes |
| [ ] | TB6600 driver B close-up | `electronics/images/IMG_TB6600_Driver_J5_MotorB_v54.jpg` | Yes |
| [ ] | Full electronics layout | `electronics/images/IMG_Electronics_Layout_v54.jpg` | Yes |
| [ ] | PSU label | `electronics/images/IMG_Dell_Server_PSU_Label_v54.jpg` | Recommended |

## Step 8 — Index update after upload

After files are uploaded, update or create:

- `hardware/design_files_index.md`
- `hardware/README.md`
- `docs/publication_checklist.md`
- `docs/hardwarex_master_checklist.md`

The design-files index should include file path, format, subsystem, BOM IDs, description and whether the file is required for replication.

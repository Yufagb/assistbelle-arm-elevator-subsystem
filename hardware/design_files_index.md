<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Mechanical design files index

This index tracks the mechanical design files currently available in the public repository.

The current uploaded CAD snapshot is **v60**. It is a working snapshot, not yet the final frozen HardwareX release. Future CAD snapshots should use their actual Fusion 360 version suffix, for example `_v61`, `_v62` or a final release tag when frozen.

## Complete assembly files

| File | Format | Subsystem | Status | Required for replication | Notes |
|---|---|---|---|---|---|
| [`cad/complete_robot/ASM_Elevator_System_v60.f3z`](cad/complete_robot/ASM_Elevator_System_v60.f3z) | Fusion 360 archive | Complete elevator assembly | Uploaded via Git LFS | Yes | Editable Fusion 360 package for the current v60 CAD snapshot. |
| [`step/ASM_Elevator_System_v60.step`](step/ASM_Elevator_System_v60.step) | STEP | Complete elevator assembly | Uploaded via Git LFS | Yes | Neutral CAD export for reviewers and users who do not use Fusion 360. |

## Pending subsystem STEP exports

Subsystem STEP exports are optional for the current working snapshot but recommended before the final HardwareX release.

| Target file | Status | Notes |
|---|---|---|
| `step/ASM_Elevator_Frame_v60.step` | Pending / optional | Fixed frame, base/top plates, V-slot profiles and structural brackets. |
| `step/ASM_Elevator_Carriage_v60.step` | Pending / optional | Moving carriage, gantry plates, spacers and V-wheel assemblies. |
| `step/ASM_Elevator_Drive_TR8_NEMA23_v60.step` | Pending / optional | NEMA23 motors, couplers, lead screws, nut blocks and supports. |
| `step/ASM_Elevator_Guide_VWheels_v60.step` | Pending / optional | Dual V-wheel guide path and wheel assemblies. |
| `step/ASM_Elevator_Electronics_Mounting_v60.step` | Pending / optional | Raspberry Pi, MCP2515 and TB6600 placement if electronics mounting is part of the CAD. |

## Pending STL exports for fabricated/printed parts

| BOM ID | Target file | Status | Notes |
|---|---|---|---|
| `FAB_ACT_002` | `stl/FAB_ACT_002_NEMA23_Mounting_Plate_ABS_v60.stl` | Pending | Required if the mounting plate is 3D printed/custom fabricated. |
| `FAB_GUI_002` | `stl/FAB_GUI_002_Spacer_Block_ABS_Gray_v60.stl` | Pending | Required if the spacer block is 3D printed/custom fabricated. |

## Pending drawings / fabrication files

| BOM ID | Target file | Status | Notes |
|---|---|---|---|
| `FAB_STR_001` | `drawings/FAB_STR_001_Base_Plate_356x356x15_MDF_v60.pdf` | Pending | MDF base plate drawing with dimensions. |
| `FAB_STR_002` | `drawings/FAB_STR_002_Top_Plate_420x400x3_StainlessSteel_v60.pdf` | Pending | Stainless steel top plate drawing with dimensions. |
| `FAB_GUI_001` | `drawings/FAB_GUI_001_Gantry_Plate_20x80_StainlessSteel_v60.pdf` | Pending | Gantry plate drawing with dimensions. |
| `FAB_STR_002` | `drawings/FAB_STR_002_Top_Plate_420x400x3_StainlessSteel_v60.dxf` | Recommended | DXF for laser/waterjet cutting if available. |
| `FAB_GUI_001` | `drawings/FAB_GUI_001_Gantry_Plate_20x80_StainlessSteel_v60.dxf` | Recommended | DXF for laser/waterjet cutting if available. |

## Pending photos

| Target file | Status | Notes |
|---|---|---|
| `photos/IMG_Elevator_Assembled_Front_v60.jpg` | Pending | Overall front view. |
| `photos/IMG_Elevator_Assembled_Side_v60.jpg` | Pending | Overall side view. |
| `photos/IMG_Elevator_Carriage_VWheels_v60.jpg` | Pending | V-wheel guide evidence. |
| `photos/IMG_Elevator_TR8_NEMA23_Drive_v60.jpg` | Pending | Lead screw, coupler and NEMA23 evidence. |
| `photos/IMG_Elevator_Top_Plate_v60.jpg` | Pending | Top plate evidence. |
| `photos/IMG_Elevator_Base_Plate_v60.jpg` | Pending | Base plate and structural bracket evidence. |

## Notes for HardwareX release

- The v60 files are a current working snapshot, not a final frozen release.
- Keep the complete `.f3z` and complete `.step` even if subsystem exports are later added.
- Do not upload individual STEP/STL files for every commercial screw, nut, bearing, motor or module unless required for reproduction.
- Before final publication, make sure the final frozen CAD version matches the BOM snapshot or clearly document any version difference.

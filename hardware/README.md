<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Hardware

Mechanical design package for the Assistbelle robotic arm and elevator subsystem.

This folder contains the mechanical files needed to reproduce the current elevator package. Do not place ROS 2 code, firmware or validation data here.

## Upload guide

Use [`design_files_index.md`](design_files_index.md) to see the current mechanical file inventory. The previous step-by-step upload plan is kept in [`design_files_upload_plan.md`](design_files_upload_plan.md) as workflow history.

## Current CAD snapshot

The current uploaded CAD snapshot is **v60**. It is a working snapshot, not yet the final frozen HardwareX release.

| File | Status | Notes |
|---|---|---|
| [`cad/complete_robot/ASM_Elevator_System_v60.f3z`](cad/complete_robot/ASM_Elevator_System_v60.f3z) | Uploaded via Git LFS | Editable Fusion 360 archive. |
| [`step/ASM_Elevator_System_v60.step`](step/ASM_Elevator_System_v60.step) | Uploaded via Git LFS | Full neutral STEP assembly. |
| [`stl/FAB_ACT_002_NEMA23_Mounting_Plate_ABS_v60.stl`](stl/FAB_ACT_002_NEMA23_Mounting_Plate_ABS_v60.stl) | Uploaded via Git LFS | NEMA 23 mounting plate STL. |
| [`stl/FAB_GUI_002_Spacer_Block_ABS_Gray_v60.stl`](stl/FAB_GUI_002_Spacer_Block_ABS_Gray_v60.stl) | Uploaded via Git LFS | Spacer block STL. |
| [`drawings/FAB_STR_001_Base_Plate_356x356x15_MDF_v60.pdf`](drawings/FAB_STR_001_Base_Plate_356x356x15_MDF_v60.pdf) | Uploaded | MDF base plate drawing. |
| [`drawings/FAB_STR_002_Top_Plate_420x400x3_StainlessSteel_v60.pdf`](drawings/FAB_STR_002_Top_Plate_420x400x3_StainlessSteel_v60.pdf) | Uploaded | Stainless-steel top plate drawing. |
| [`drawings/FAB_GUI_001_Gantry_Plate_127x88x3_StainlessSteel_v60.pdf`](drawings/FAB_GUI_001_Gantry_Plate_127x88x3_StainlessSteel_v60.pdf) | Uploaded | Stainless-steel gantry plate drawing. |
| [`drawings/FAB_STR_002_Top_Plate_420x400x3_StainlessSteel_v60.dxf`](drawings/FAB_STR_002_Top_Plate_420x400x3_StainlessSteel_v60.dxf) | Uploaded via Git LFS | Top plate cutting DXF. |
| [`drawings/FAB_GUI_001_Gantry_Plate_127x88x3_StainlessSteel_v60.dxf`](drawings/FAB_GUI_001_Gantry_Plate_127x88x3_StainlessSteel_v60.dxf) | Uploaded via Git LFS | Gantry plate cutting DXF. |

## Canonical structure

| Folder | Content |
|---|---|
| `cad/` | Editable CAD files. |
| `step/` | Neutral STEP exports. |
| `stl/` | 3D-printable or fabricated-part exports. |
| `drawings/` | Mechanical drawings and DXF cutting files. |
| `photos/` | Photos of the assembled mechanical system. Deferred until robot access. |
| `fasteners/` | Screws, nuts, bearings, profiles and standard mechanical parts. |

## CAD substructure

| Folder | Content |
|---|---|
| `cad/complete_robot/` | Complete assembly. |
| `cad/arm/` | 4-DOF arm, joints and links, if exported separately. |
| `cad/elevator/` | Vertical elevator mechanism, if exported separately. |
| `cad/gripper/` | End effector or gripper, if exported separately. |
| `cad/mounts/` | Mounts, adapters and brackets, if exported separately. |

## Legacy folders

Older folders such as `CAD_editable`, `STEP` and `STL` were created during previous passes. For new files, use only the canonical lowercase folders: `cad`, `step` and `stl`.

## Minimum publication requirement

Each custom mechanical part should have at least one of the following:

- editable CAD file;
- STEP export;
- STL file if it is 3D printed;
- drawing with dimensions;
- DXF file if it is a cut plate;
- photo showing the part installed when physical access is available.

## Remaining mechanical work

- Add physical prototype photos once the robot is accessible.
- Optionally add subsystem STEP exports before the final frozen release.
- Re-export changed CAD/STEP/STL/PDF/DXF files if the snapshot advances beyond v60.
- Freeze the final CAD/BOM version before HardwareX submission.

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Hardware

Mechanical design package for the Assistbelle robotic arm and elevator subsystem.

This folder should contain only the mechanical files needed to reproduce the robot. Do not place ROS 2 code, firmware or validation data here.

## Upload guide

Follow [`design_files_upload_plan.md`](design_files_upload_plan.md) to upload the mechanical package step by step. Use [`design_files_index.md`](design_files_index.md) to see which files are already uploaded and which are pending.

## Current CAD snapshot

The current uploaded CAD snapshot is **v60**. It is a working snapshot, not yet the final frozen HardwareX release.

| File | Status | Notes |
|---|---|---|
| [`cad/complete_robot/ASM_Elevator_System_v60.f3z`](cad/complete_robot/ASM_Elevator_System_v60.f3z) | Uploaded | Editable Fusion 360 archive tracked through Git LFS. |
| [`step/ASM_Elevator_System_v60.step`](step/ASM_Elevator_System_v60.step) | Uploaded | Full neutral STEP assembly tracked through Git LFS. |

## Canonical structure

| Folder | Content |
|---|---|
| `cad/` | Editable CAD files. |
| `step/` | Neutral STEP exports. |
| `stl/` | 3D-printable files. |
| `drawings/` | Mechanical drawings with dimensions. |
| `photos/` | Photos of the assembled mechanical system. |
| `fasteners/` | Screws, nuts, bearings, profiles and standard mechanical parts. |

## CAD substructure

| Folder | Content |
|---|---|
| `cad/complete_robot/` | Complete assembly. |
| `cad/arm/` | 4-DOF arm, joints and links. |
| `cad/elevator/` | Vertical elevator mechanism. |
| `cad/gripper/` | End effector or gripper. |
| `cad/mounts/` | Mounts, adapters and brackets. |

## Legacy folders

Older folders such as `CAD_editable`, `STEP` and `STL` were created during previous passes. For new files, use only the canonical lowercase folders: `cad`, `step` and `stl`.

## Minimum publication requirement

Each custom mechanical part should have at least one of the following:

- editable CAD file;
- STEP export;
- STL file if it is 3D printed;
- drawing with dimensions;
- photo showing the part installed.

## Current next upload target

The next useful mechanical upload is the STL export for the fabricated/printed NEMA 23 mounting plate:

```text
hardware/stl/FAB_ACT_002_NEMA23_Mounting_Plate_ABS_v60.stl
```

Then upload the spacer block STL:

```text
hardware/stl/FAB_GUI_002_Spacer_Block_ABS_Gray_v60.stl
```

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Mechanical figure plan

Planning document for the mechanical figure(s) needed in the HardwareX manuscript.

Physical prototype photographs are currently deferred because the robot is not available for imaging. Until then, CAD screenshots/renders from the v60 working snapshot can be used as temporary manuscript figure drafts.

## Recommended mechanical figures

| Figure | Preferred source | Temporary source | Status |
|---|---|---|---|
| Full elevator assembly | Physical front/side photo | Fusion 360 render from `ASM_Elevator_System_v60.f3z` | Pending. |
| CAD overview | Fusion 360 render | Fusion 360 screenshot | Pending. |
| Base and top plate detail | Physical close-up photo | PDF drawing + CAD crop | Pending. |
| Carriage / V-wheel detail | Physical close-up photo | CAD crop around gantry plate and V-wheels | Pending. |
| TR8/NEMA23 drive detail | Physical close-up photo | CAD crop around NEMA23, coupler and TR8 screw | Pending. |
| Custom fabricated parts | Drawing + CAD view | `hardware/drawings/` and `hardware/stl/` | Partially ready. |

## Suggested CAD-render checklist

When exporting temporary CAD renders from Fusion 360:

1. Open `ASM_Elevator_System_v60.f3z`.
2. Use the v60 snapshot without further geometric changes unless the snapshot version is incremented.
3. Export one front/isometric render of the full elevator assembly.
4. Export one close-up of the moving carriage and V-wheel guide.
5. Export one close-up of the TR8 lead screw, coupler and NEMA 23 motor region.
6. Export one detail of base/top/gantry fabricated plates if useful.
7. Save images under `paper/figures/exported/` or `hardware/photos/` depending on whether they are CAD renders or real photos.

## Suggested file names

| Figure file | Type | Planned location |
|---|---|---|
| `fig_mechanical_overview_v60.png` | CAD render | `paper/figures/exported/` |
| `fig_elevator_carriage_vwheels_v60.png` | CAD render | `paper/figures/exported/` |
| `fig_elevator_tr8_nema23_drive_v60.png` | CAD render | `paper/figures/exported/` |
| `fig_fabricated_plates_v60.png` | CAD/drawing composite | `paper/figures/exported/` |
| `IMG_Elevator_Assembled_Front_v60.jpg` | Physical photo | `hardware/photos/` |
| `IMG_Elevator_Assembled_Side_v60.jpg` | Physical photo | `hardware/photos/` |
| `IMG_Elevator_Carriage_VWheels_v60.jpg` | Physical photo | `hardware/photos/` |
| `IMG_Elevator_TR8_NEMA23_Drive_v60.jpg` | Physical photo | `hardware/photos/` |

## Caption draft

**Figure X. Mechanical design of the vertical elevator subsystem.** The elevator is based on a V-slot frame, dual TR8 lead-screw actuation driven by two NEMA 23 stepper motors, and a guided moving carriage using V-wheel assemblies and custom fabricated plates. The current public CAD package is provided as the v60 working snapshot and includes editable Fusion 360 and neutral STEP files, STL files for custom printed/fabricated parts, and PDF/DXF fabrication files for plates.

## Open items

- Export CAD renders from the current v60 assembly.
- Add physical photos once the robot is accessible.
- Replace temporary CAD screenshots with final high-resolution renders/photos before submission.
- Confirm final frozen CAD release before producing manuscript-ready figures.

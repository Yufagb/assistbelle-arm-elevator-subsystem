<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Validation data index

This file summarizes the curated validation evidence currently stored in the repository.

## Uploaded evidence

| Evidence group | Repository path | Status |
|---|---|---|
| Joint-motion CSV/TXT data | `validation/joint_motion_tests/raw/` | Uploaded. |
| Joint-motion plots | `validation/joint_motion_tests/plots/` | Uploaded. |
| Kinematics figures | `validation/kinematics_tests/figures/` | Uploaded. |
| Perception figures | `validation/perception_tests/figures/` | Uploaded. |
| Joint-motion Tracker projects and linked videos | `validation/tracker_files/joint_motion/` | Uploaded through Git LFS. Each tracked `.trk` has its linked `.mp4` in the same folder. |
| Kinematics Tracker projects and linked images | `validation/tracker_files/kinematics/` | Uploaded through Git LFS. Each tracked `.trk` has its linked `.jpeg` in the same folder. |
| Representative validation videos | `validation/media/` | Uploaded through Git LFS for quick reviewer access. |

## Representative videos uploaded

| Evidence group | File | Purpose |
|---|---|---|
| J5 ramp motion | `validation/media/joint_motion/j5_ramp_100.0mm_5reps_robot.mp4` | Elevator response with ramp profile. |
| J5 trapezoidal motion | `validation/media/joint_motion/j5_trap_100.0mm_5reps_robot.mp4` | Elevator response with trapezoidal profile. |
| J1 step motion | `validation/media/joint_motion/j1_step_30.0deg_5reps_robot.mp4` | Representative revolute joint step response. |
| Perception | `validation/media/perception/resultado_percepcion_video_prueba_completa.mp4` | Representative perception test. |
| Teleoperation | `validation/media/teleoperation/Teclado_P2.mp4` | Representative keyboard teleoperation test. |

## Tracker-linked media uploaded

The repository also stores validation media next to the Tracker project files so that reviewers can open each `.trk` directly after cloning with Git LFS enabled.

| Tracker group | Linked media stored next to `.trk` | Purpose |
|---|---:|---|
| Joint motion | 15 `.mp4` files | Full Tracker-linked video evidence for J1-J5 step, ramp and trapezoidal motion tests. |
| Kinematics | 20 `.jpeg` files | Tracker-linked still-image evidence for inverse/direct kinematics measurement cases P1-P5. |

## Local video evidence not yet committed

The historical `resultados/` folder may still contain additional raw videos and intermediate files. These are kept outside the repository unless they are needed for reproducibility or review.

| Local folder | Current decision |
|---|---|
| `validation/media/joint_motion/` | Representative videos uploaded in `validation/media/`; full Tracker-linked set uploaded in `validation/tracker_files/joint_motion/`. |
| `validation/media/kinematics/` | Tracker-linked `.jpeg` evidence uploaded in `validation/tracker_files/kinematics/`. |
| `validation/media/teleoperation/` | Representative `Teclado_P2.mp4` uploaded. Remaining videos can stay local unless needed. |
| `validation/media/perception/` | Main perception video uploaded. |

## Recommended next step

Use `paper/tables/validation_summary.md` as the manuscript-facing summary of the uploaded validation evidence. Keep any remaining raw video material either local or in an external archive if full audiovisual provenance is required.

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
| Joint-motion Tracker files | `validation/tracker_files/joint_motion/` | Uploaded through Git LFS. |
| Kinematics Tracker files | `validation/tracker_files/kinematics/` | Uploaded through Git LFS. |
| Representative validation videos | `validation/media/` | Uploaded through Git LFS. |

## Representative videos uploaded

| Evidence group | File | Purpose |
|---|---|---|
| J5 ramp motion | `validation/media/joint_motion/j5_ramp_100.0mm_5reps_robot.mp4` | Elevator response with ramp profile. |
| J5 trapezoidal motion | `validation/media/joint_motion/j5_trap_100.0mm_5reps_robot.mp4` | Elevator response with trapezoidal profile. |
| J1 step motion | `validation/media/joint_motion/j1_step_30.0deg_5reps_robot.mp4` | Representative revolute joint step response. |
| Perception | `validation/media/perception/resultado_percepcion_video_prueba_completa.mp4` | Representative perception test. |
| Teleoperation | `validation/media/teleoperation/Teclado_P2.mp4` | Representative keyboard teleoperation test. |

## Local video evidence not yet committed

The full video set remains available locally after copying from the historical `resultados/` folder, but only a representative subset was committed because the complete set is large.

| Local folder | Approximate size before subset selection | Current decision |
|---|---:|---|
| `validation/media/joint_motion/` | 931 MB | Representative subset uploaded; remaining videos stay local or can be linked externally. |
| `validation/media/kinematics/` | 468 MB | Not uploaded; select later or link externally if needed. |
| `validation/media/teleoperation/` | 351 MB | Representative `Teclado_P2.mp4` uploaded; remaining videos stay local or can be linked externally. |
| `validation/media/perception/` | 12 MB | Main perception video uploaded. |

## Recommended next step

Use the uploaded subset for the manuscript and HardwareX review package. Keep the complete video set either local or in an external archive if full audiovisual reproducibility is required.

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Validation summary table

This table summarizes the validation evidence available in the repository for the HardwareX manuscript and reviewer package. Tracker-linked media are stored next to their `.trk` files to support direct inspection after cloning with Git LFS enabled.

| Validation test | Data file(s) | Plot / figure evidence | Tracker / media evidence | What it demonstrates |
|---|---|---|---|---|
| J5 ramp motion | `validation/joint_motion_tests/raw/j5_ramp_100.0mm_5reps.csv` and related Tracker text exports | `validation/joint_motion_tests/plots/j5_ramp_100.0mm_5reps*.png` | `validation/tracker_files/joint_motion/j5_ramp_100.0mm_5reps_robot.trk` with `j5_ramp_100.0mm_5reps_robot.mp4` | Elevator axis follows a 100 mm ramp motion profile. |
| J5 trapezoidal motion | `validation/joint_motion_tests/raw/j5_trap_100.0mm_5reps.csv` and related Tracker text exports | `validation/joint_motion_tests/plots/j5_trap_100.0mm_5reps*.png` | `validation/tracker_files/joint_motion/j5_trap_100.0mm_5reps_robot.trk` with `j5_trap_100.0mm_5reps_robot.mp4` | Elevator axis follows a 100 mm trapezoidal motion profile. |
| J5 step motion | `validation/joint_motion_tests/raw/j5_step_100.0mm_5reps.csv` and related Tracker text exports | `validation/joint_motion_tests/plots/j5_step_100.0mm_5reps*.png` | `validation/tracker_files/joint_motion/j5_step_100.0mm_5reps_robot.trk` with `j5_step_100.0mm_5reps_robot.mp4` | Elevator axis responds to a 100 mm step command. |
| J1 step motion | `validation/joint_motion_tests/raw/j1_step_30.0deg_5reps.csv` and related Tracker text exports | `validation/joint_motion_tests/plots/j1_step_30.0deg_5reps*.png` | `validation/tracker_files/joint_motion/j1_step_30.0deg_5reps_robot.trk` with `j1_step_30.0deg_5reps_robot.mp4` | Representative revolute joint responds to a 30 degree step command. |
| J1-J4 ramp and trapezoidal motion | `validation/joint_motion_tests/raw/j*_ramp_*.csv`, `validation/joint_motion_tests/raw/j*_trap_*.csv` and related Tracker text exports | `validation/joint_motion_tests/plots/j*_ramp_*.png`, `validation/joint_motion_tests/plots/j*_trap_*.png` | `validation/tracker_files/joint_motion/` | Revolute joints J1-J4 execute the evaluated motion profiles with recorded physical evidence. |
| Kinematics P1-P5 | Kinematic measurement exports in `validation/tracker_files/kinematics/` and figures in `validation/kinematics_tests/figures/` | `validation/kinematics_tests/figures/` | `validation/tracker_files/kinematics/*.trk` with linked `.jpeg` files stored in the same folder | Direct/inverse kinematics measurement cases are documented with Tracker projects and image evidence. |
| Perception test | Perception figures in `validation/perception_tests/figures/` | `validation/perception_tests/figures/` | `validation/media/perception/resultado_percepcion_video_prueba_completa.mp4` | Perception pipeline can detect or identify the target in the representative test. |
| Teleoperation test | Not applicable | Not applicable | `validation/media/teleoperation/Teclado_P2.mp4` | Manual keyboard control through the software stack produces physical robot motion. |

## Notes for reviewers

- To open Tracker projects, install Tracker Video Analysis and clone the repository with Git LFS enabled.
- For joint-motion tests, open the `.trk` files in `validation/tracker_files/joint_motion/`; their linked `.mp4` files are stored in the same folder.
- For kinematics tests, open the `.trk` files in `validation/tracker_files/kinematics/`; their linked `.jpeg` files are stored in the same folder.
- Representative videos are also mirrored under `validation/media/` for quick inspection without opening Tracker.

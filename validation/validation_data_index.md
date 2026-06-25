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

## Local video evidence not yet committed

The video folders below exist in the local working tree after copying from the historical `resultados/` folder, but they were intentionally not committed because the full video set is large.

| Local folder | Approximate size | Current decision |
|---|---:|---|
| `validation/media/joint_motion/` | 931 MB | Select a representative subset or link externally. |
| `validation/media/kinematics/` | 468 MB | Select a representative subset or link externally. |
| `validation/media/teleoperation/` | 351 MB | Select a representative subset or link externally. |
| `validation/media/perception/` | 12 MB | Candidate for Git LFS upload. |

## Recommended next step

Choose a small representative video subset for the manuscript and HardwareX reviewers. Keep the complete video set either local or in an external archive if total size is too large for the repository.

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# License overview

This repository uses a multi-license structure for the HardwareX publication package.

## License policy

| Area | License | File |
|---|---|---|
| `hardware/` and `electronics/` | CERN-OHL-S-2.0 | `LICENSES/CERN-OHL-S-2.0.txt` |
| `firmware/`, `ros2_ws/`, `software/` and validation scripts | Apache-2.0 | `LICENSES/Apache-2.0.txt` |
| `docs/`, `paper/`, images, figures and manuals | CC-BY-4.0 | `LICENSES/CC-BY-4.0.txt` |

## SPDX identifiers

Use these identifiers when adding new files:

- `SPDX-License-Identifier: CERN-OHL-S-2.0` for mechanical and electronic hardware design files.
- `SPDX-License-Identifier: Apache-2.0` for firmware, ROS 2 software and validation scripts.
- `SPDX-License-Identifier: CC-BY-4.0` for documentation, figures, manuals and paper material.

If a file format does not support comments, the applicable license is defined by its directory and by the root `LICENSE` file.

## Notes

The root `LICENSE` file summarizes this policy. Full or reference license texts are kept in the `LICENSES/` directory.

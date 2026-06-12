# License overview

This repository currently uses **Apache-2.0** as the main repository license through the top-level [`LICENSE`](../LICENSE) file.

## Index

- [Current license status](#current-license-status)
- [Citation](#citation)
- [Future refinement](#future-refinement)

## Current license status

| Asset type | Current status | Notes |
|---|---|---|
| ROS 2 software | Apache-2.0 | `can_comm_pkg` declares Apache-2.0 in its package metadata. |
| ESP32 firmware | Apache-2.0 | Covered by the top-level repository license. |
| Documentation | Apache-2.0 for now | Can later be moved to CC-BY-4.0 if required by the publication venue. |
| Media and validation files | Apache-2.0 for now | If external videos are used, their storage and reuse conditions must be documented. |
| CAD / mechanical files | Pending | Recommended license: CERN-OHL-S-2.0 when CAD files are added. |

## Citation

Citation metadata is available in the top-level file [`CITATION.cff`](../CITATION.cff).

The `repository-code` field points to the public repository:

```text
https://github.com/Yufagb/assistbelle-arm-elevator-subsystem
```

## Future refinement

Before final publication, decide whether to keep a single license for simplicity or use a split-license model:

- software and firmware: Apache-2.0;
- hardware design files: CERN-OHL-S-2.0;
- documentation and media: CC-BY-4.0.

For the current public preparation repository, Apache-2.0 is the active repository license.

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Repository cleanup audit

Repository cleanup audit for the HardwareX preparation workflow.

## Audit scope

This audit covers checks that can be performed from the GitHub repository view plus a local command checklist for checks that require a clone.

## Remote checks performed

| Check | Result | Action taken |
|---|---|---|
| ROS placeholder email for `can_comm_pkg` | Found in package metadata and an obsolete backup file. | Replaced in current `setup.py` and `package.xml`; removed `setup.py.bak`. |
| ROS placeholder email for `video_streamer` | Found in package metadata. | Replaced with project maintainer metadata. |
| ROS placeholder package description | Found in `video_streamer` and `cpp_video_streamer`. | Replaced with project-specific descriptions. |
| ROS placeholder license declaration | Found in `video_streamer`, `cpp_robot_control` and `cpp_video_streamer`. | Replaced with `Apache-2.0`. |
| Local backup files | `setup.py.bak` was tracked. | Removed tracked backup and added `*.bak`, `*.tmp`, `*.orig` to `.gitignore`. |
| Generated folders search | No obvious tracked `build/`, `install/`, `log/`, `.vscode` or `.idea` files found by repository text search. | Local `git ls-files` check completed by the project owner and returned OK. |

## Files cleaned

| File | Cleanup |
|---|---|
| `ros2_ws/src/can_comm_pkg/setup.py` | Maintainer email corrected. |
| `ros2_ws/src/can_comm_pkg/package.xml` | Description and maintainer email corrected. |
| `ros2_ws/src/can_comm_pkg/setup.py.bak` | Removed as obsolete tracked backup. |
| `ros2_ws/src/video_streamer/setup.py` | Maintainer, email, description and license metadata corrected. |
| `ros2_ws/src/video_streamer/package.xml` | Description, maintainer, email and license metadata corrected. |
| `ros2_ws/src/cpp_robot_control/package.xml` | Maintainer name and license metadata corrected. |
| `ros2_ws/src/cpp_video_streamer/package.xml` | Description, maintainer, email and license metadata corrected. |
| `.gitignore` | Added local backup-file patterns. |

## Local validation results

The project owner ran the following local checks after pulling the latest `main` branch:

```text
git status -> nothing to commit, working tree clean
no tracked generated/local-state files found
no tracked backup/temp files found
```

The placeholder grep returned matches only inside this audit document, because this file documents the cleanup history and the validation command itself. The command below excludes this audit file to avoid that intentional false positive.

## Local validation commands for future runs

Run these commands from the repository root after pulling the latest `main` branch:

```bash
git pull
git status
```

Check for tracked generated folders or local-state files:

```bash
git ls-files | grep -E '(^|/)(build|install|log|\.vscode|\.idea|__pycache__|\.pytest_cache|\.mypy_cache)(/|$)' || echo "OK: no tracked generated/local-state files found"
```

Check for tracked backup or temporary files:

```bash
git ls-files | grep -E '\.(bak|tmp|orig)$' || echo "OK: no tracked backup/temp files found"
```

Check for remaining obvious publication-placeholder strings while excluding this audit file:

```bash
git grep -n -E 'tu_email@ejemplo\.com|rosario@todo\.todo|TODO: Package description|TODO: License declaration|CHANGE_ME|ADD_ME|YOUR_EMAIL|example\.com|ejemplo\.com' -- . ':!docs/repo_cleanup_audit.md' || echo "OK: no obvious publication placeholders found"
```

Check for broader TODO/FIXME markers. Not all results are errors; some may be intentional engineering notes:

```bash
git grep -n -E 'TODO|FIXME|TBD|PLACEHOLDER' || echo "OK: no TODO/FIXME/TBD/PLACEHOLDER markers found"
```

Check Git LFS tracking for CAD/fabrication files:

```bash
git check-attr filter -- \
  hardware/cad/complete_robot/ASM_Elevator_System_v60.f3z \
  hardware/step/ASM_Elevator_System_v60.step \
  hardware/stl/FAB_ACT_002_NEMA23_Mounting_Plate_ABS_v60.stl \
  hardware/stl/FAB_GUI_002_Spacer_Block_ABS_Gray_v60.stl \
  hardware/drawings/FAB_STR_002_Top_Plate_420x400x3_StainlessSteel_v60.dxf \
  hardware/drawings/FAB_GUI_001_Gantry_Plate_127x88x3_StainlessSteel_v60.dxf
```

Expected output for those large CAD/fabrication assets:

```text
filter: lfs
```

## Remaining cleanup work

- Run the placeholder check with the audit-file exclusion command above.
- Review broader `TODO` results manually; many may be valid engineering TODOs rather than publication placeholders.
- Check Markdown links before final HardwareX submission.
- Run a clean-clone ROS 2 build test for `can_comm_pkg` and other active packages.

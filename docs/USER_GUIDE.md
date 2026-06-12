# User Guide

## 🎮 Teleoperation

Control the robot using the keyboard.

```bash
ros2 run can_comm_pkg control_teclado
```

*   **Keys**:
    *   `1`/`Q`: J1 +/-
    *   `2`/`W`: J2 +/-
    *   `3`/`E`: J3 +/-
    *   `4`/`R`: J4 +/-
    *   `5`/`T`: J5 +/-

## 📈 Trajectory Generation

Launch the GUI to design and execute trajectories.

```bash
ros2 run can_comm_pkg can_traj
```

1.  **Home**: Moves robot to zero position.
2.  **Add Point**: Adds current configuration to trajectory.
3.  **Generate**: Creates a smooth path (LSPB/Trapezoidal).
4.  **Execute**: Sends commands to the robot.

## 🧪 Performance Testing

Run automated tests to verify joint performance.

**Syntax:**
```bash
ros2 run can_comm_pkg j<JOINT>_<PROFILE>
```

**Available Tests:**
*   **Joints**: `j1`, `j2`, `j3`, `j4`, `j5`
*   **Profiles**: `step`, `ramp`, `trap`

**Example:**
```bash
ros2 run can_comm_pkg j5_step
```
*   Prompts for Target (mm) and Time.
*   Executes 5 repetitions.
*   Saves data and plots to `resultados/`.

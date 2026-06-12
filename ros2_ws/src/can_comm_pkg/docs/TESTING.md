# Robot Performance Testing Suite

This package includes a set of automated scripts to test the step response, ramp response, and trapezoidal profile tracking for each joint (J1-J5).

## Features

*   **Automated Execution**: Runs a specified number of repetitions for each test.
*   **Data Recording**: Captures Setpoint vs. Measured data for Position, Velocity, and Acceleration.
*   **Advanced Processing**:
    *   **Savitzky-Golay Filtering**: Smooths noisy encoder data.
    *   **Robust Differentiation**: Calculates clean velocity and acceleration derivatives.
*   **Visualization**: Generates plots with error curves.
*   **Data Export**: Automatically saves `.csv` data and `.png` plots to a `resultados` folder.

## Usage

The tests are registered as ROS 2 executables. You can run them using `ros2 run`.

### Command Format

```bash
ros2 run can_comm_pkg j<JOINT>_<PROFILE>
```

*   **JOINT**: `1`, `2`, `3`, `4`, `5`
*   **PROFILE**: `step`, `ramp`, `trap`

### Examples

*   **J1 Step Response**:
    ```bash
    ros2 run can_comm_pkg j1_step
    ```
*   **J4 Trapezoidal Profile**:
    ```bash
    ros2 run can_comm_pkg j4_trap
    ```
*   **J5 Ramp Response**:
    ```bash
    ros2 run can_comm_pkg j5_ramp
    ```

## Parameters

When you run a test, you will be prompted for:

1.  **Target**:
    *   For **J1-J4** (Rotational): Target position in **degrees**.
    *   For **J5** (Linear): Target position in **millimeters**.
2.  **Time**: Duration of the movement in seconds.
3.  **Repetitions**: Number of back-and-forth cycles to perform.

## Output

Results are saved in the `resultados` folder within the directory where you executed the command.

**Files Generated:**
*   `jX_type_TARGET_REPS.csv`: Raw and processed data.
*   `jX_type_TARGET_REPS.png`: Plot of Position, Velocity, and Acceleration with errors.

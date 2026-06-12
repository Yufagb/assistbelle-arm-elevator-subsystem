# Node Documentation

## `can_node`

The central communication hub.
*   **Subscribes to**: `/can_command` (std_msgs/String)
*   **Publishes to**: `/joint_states` (sensor_msgs/JointState), `/motors_state` (std_msgs/Float32MultiArray)
*   **Function**: Reads from the CAN bus (using `python-can`), parses motor messages, and broadcasts the robot state. Accepts commands to drive motors.

## `can_traj`

A Tkinter-based GUI for offline trajectory generation.
*   **Features**:
    *   Visualizes trajectories before execution.
    *   Sends synchronized commands to all joints.
    *   Records data for analysis.
    *   Implements Savitzky-Golay filtering for smooth velocity/acceleration plots.

## `can_cli`

A simple command-line interface for testing individual motor commands.
*   **Usage**: `ros2 run can_comm_pkg can_cli`
*   **Commands**:
    *   `C1-C4`: Position/Velocity control for rotational joints.
    *   `C5`: Position control for linear joint (mm).
    *   `D2`: Gripper control.

## `control_teclado`

Teleoperation node.
*   **Usage**: `ros2 run can_comm_pkg control_teclado`
*   **Controls**: Use keyboard keys to move joints.

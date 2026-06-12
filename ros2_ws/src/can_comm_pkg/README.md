# CAN Communication Package (`can_comm_pkg`)

This package provides a ROS 2 interface for controlling a 5-DOF robot arm via CAN bus. It includes nodes for low-level communication, trajectory generation, teleoperation, and a comprehensive performance testing suite.

## Installation

1.  Clone the repository into your ROS 2 workspace `src` folder.
2.  Install dependencies:
    ```bash
    pip install python-can
    rosdep install --from-paths src --ignore-src -r -y
    ```
3.  Build the package:
    ```bash
    colcon build --packages-select can_comm_pkg
    source install/setup.bash
    ```

## Key Nodes

*   **`can_node`**: The core driver node. Handles CAN bus communication, sends commands to motors, and publishes joint states.
*   **`can_traj`**: GUI application for trajectory generation and visualization.
*   **`can_cli`**: Command Line Interface for sending direct commands to joints.
*   **`control_teclado`**: Teleoperation node using keyboard input.

## Testing Suite

A comprehensive test suite is available to validate the performance of each joint (J1-J5) using Step, Ramp, and Trapezoidal profiles.

See [docs/TESTING.md](docs/TESTING.md) for detailed usage instructions.

## Documentation

*   [Node Descriptions](docs/NODES.md)
*   [Testing Guide](docs/TESTING.md)

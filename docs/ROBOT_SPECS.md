# Robot Specifications

## 🦾 Joint Limits

The robot consists of a prismatic base (J5/Ascensor) and a 4-DOF articulated arm (J1-J4).

| Joint | Type | Name | Min Limit | Max Limit | Unit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **J1** | Revolute | Base | -135° | +34° | Degrees |
| **J2** | Revolute | Shoulder | -45° | +70° | Degrees |
| **J3** | Revolute | Elbow | -140° | +120° | Degrees |
| **J4** | Revolute | Wrist | -180° | +180° | Degrees |
| **J5** | Prismatic | Elevator | 0 mm | 350 mm | Millimeters |

> **Note**: J5 is physically the base elevator, but is often addressed as index 5 or 0 in different contexts. In the CAN protocol, it is Motor 5.

## 📐 Denavit-Hartenberg (DH) Parameters

The kinematic chain is defined as follows:

| Link | $\theta$ (Offset) | $d$ (m) | $a$ (m) | $\alpha$ (rad) |
| :--- | :--- | :--- | :--- | :--- |
| **0 (Elevator)** | 0 | $d_0 + 0.4$ | 0 | 0 |
| **1 (Base)** | $\theta_1 + 360^\circ$ | 0 | 0 | -90° |
| **2 (Fixed)** | $180^\circ$ | 0.1 | 0 | 0 |
| **3 (Shoulder)** | $\theta_2 + 180^\circ$ | 0 | 0.215 | 0 |
| **4 (Elbow)** | $\theta_3$ | 0 | 0.25 | 180° |
| **5 (Wrist)** | $\theta_4$ | 0 | 0.125 | 90° |

## 🔌 Hardware Interface

*   **Bus**: CAN Bus (Controller Area Network)
*   **Bitrate**: 1 Mbps (typical)
*   **Interface**: `can0` (SocketCAN)
*   **Motors**: Custom actuators with integrated controllers.

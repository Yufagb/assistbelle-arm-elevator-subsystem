<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# System architecture figure draft

Draft Mermaid diagram for the HardwareX manuscript. This figure describes the current open-source package scope: Raspberry Pi 5, ROS 2, CAN bus, distributed ESP32 nodes, motor drivers and the vertical elevator/mechanical subsystem.

```mermaid
flowchart LR
    subgraph HOST[High-level computer]
        RPI[Raspberry Pi 5\nROS 2 / can_comm_pkg]
        MCP[MCP2515 CAN-SPI module\n500 kbit/s CAN]
        RPI -->|SPI + INT| MCP
    end

    subgraph BUS[Main CAN bus]
        CAN[(CANH / CANL\nRT1 + RT2 termination)]
    end

    MCP -->|CANH/CANL| CAN

    subgraph CTRL[Distributed ESP32 control nodes]
        J1[J1 ESP32\nBase joint]
        J2[J2 ESP32\nShoulder joint]
        J3[J3 ESP32\nElbow joint]
        J4[J4 ESP32\nWrist + gripper]
        J5[J5 ESP32\nVertical elevator]
    end

    CAN --> J1
    CAN --> J2
    CAN --> J3
    CAN --> J4
    CAN --> J5

    subgraph DRV[Motor drivers]
        D1[DRV8871\nJ1]
        D2[IBT-2 / BTS7960\nJ2]
        D3[IBT-2 / BTS7960\nJ3]
        D4[DRV8871 + servo\nJ4 / gripper]
        D5A[TB6600 Motor A\nJ5]
        D5B[TB6600 Motor B\nJ5]
    end

    J1 --> D1
    J2 --> D2
    J3 --> D3
    J4 --> D4
    J5 -->|PUL/DIR/ENA shared| D5A
    J5 -->|PUL/DIR/ENA shared| D5B

    subgraph MECH[Mechanical subsystem]
        ARM[Robotic arm joints\nJ1-J4]
        ELEV[Dual-NEMA23 TR8 vertical elevator\nV-slot + V-wheel guide]
        GRIP[End-effector / gripper]
    end

    D1 --> ARM
    D2 --> ARM
    D3 --> ARM
    D4 --> ARM
    D4 --> GRIP
    D5A --> ELEV
    D5B --> ELEV
```

## Manuscript caption draft

**Figure X. System architecture of the Assistbelle arm and vertical elevator subsystem.** A Raspberry Pi 5 runs ROS 2 and interfaces with the CAN network through an MCP2515 CAN-SPI module. Distributed ESP32 nodes receive CAN commands and control joint-level motor drivers. The J5 elevator node drives two TB6600 stepper drivers in parallel using shared PUL/DIR/ENA signals to synchronize two NEMA 23 motors.

## Notes before final figure export

- Replace this Mermaid draft with a vector SVG/PDF figure before final submission if required.
- Keep the J5 `B5` CAN payload compatibility note in the text until firmware/ROS is finalized.
- Add physical photos or CAD render callouts when the final release is frozen.

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Electronics and CAN architecture figure draft

Draft Mermaid diagram for the electronics/CAN figure in the HardwareX manuscript.

```mermaid
flowchart TB
    subgraph RPI_SIDE[Raspberry Pi side]
        RPI[Raspberry Pi 5\nROS 2]
        SPI[SPI0\nMOSI / MISO / SCK / CE0]
        INT[INT_CAN\nGPIO25]
        MCP[MCP2515 module\n5 V module power\n3.3 V SPI/INT compatibility required]
        RPI --> SPI --> MCP
        MCP --> INT --> RPI
    end

    subgraph CANBUS[CAN physical bus]
        RT1[120 ohm RT1\nphysical end]
        CANH[CANH]
        CANL[CANL]
        RT2[120 ohm RT2\nphysical end]
        RT1 --- CANH
        RT1 --- CANL
        CANH --- RT2
        CANL --- RT2
    end

    MCP -->|CANH/CANL| CANBUS

    subgraph NODES[ESP32 CAN nodes]
        N1[J1 ESP32\nCAN TX/RX]
        N2[J2 ESP32\nCAN TX/RX]
        N3[J3 ESP32\nCAN TX/RX]
        N4[J4 ESP32\nCAN TX/RX]
        N5[J5 ESP32\nCAN TX=GPIO22\nCAN RX=GPIO21]
    end

    CANBUS --> N1
    CANBUS --> N2
    CANBUS --> N3
    CANBUS --> N4
    CANBUS --> N5

    subgraph DRIVERS[Driver interfaces]
        DRV1[DRV8871\nJ1]
        IBT2A[IBT-2 / BTS7960\nJ2]
        IBT2B[IBT-2 / BTS7960\nJ3]
        DRV4[DRV8871 + servo\nJ4]
        TB1[TB6600 Motor A\nJ5]
        TB2[TB6600 Motor B\nJ5]
    end

    N1 --> DRV1
    N2 --> IBT2A
    N3 --> IBT2B
    N4 --> DRV4
    N5 -->|GPIO5 PUL| TB1
    N5 -->|GPIO18 DIR| TB1
    N5 -->|GPIO19 ENA| TB1
    N5 -->|GPIO5 PUL| TB2
    N5 -->|GPIO18 DIR| TB2
    N5 -->|GPIO19 ENA| TB2
```

## Manuscript caption draft

**Figure X. Electronics and CAN communication architecture.** The Raspberry Pi 5 communicates with the distributed ESP32 motor-control nodes through an MCP2515 CAN-SPI interface. The CAN bus uses CANH/CANL differential signaling with 120-ohm terminations at the intended physical ends of the bus. The J5 elevator node distributes the same PUL, DIR and ENA signals to two TB6600 drivers for synchronized dual-motor elevator motion.

## Open items before final figure export

- Confirm physical positions of RT1 and RT2.
- Confirm CANH/CANL orientation in every branch connector.
- Confirm exact MCP2515 module model and 3.3 V SPI/INT compatibility.
- Confirm exact connector types, pin order and wire colors when the robot is available.

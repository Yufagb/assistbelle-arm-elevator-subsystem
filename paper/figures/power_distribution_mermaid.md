<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Power distribution figure draft

Draft Mermaid diagram for the HardwareX power-distribution figure.

```mermaid
flowchart LR
    PSU[Dell server PSU\n12 V actuator supply\nexact model pending]
    BUCK[LM2596S DC-DC buck\n5 V logic rail]
    ESTOP[Panic / emergency button\ninterrupts actuator power]

    subgraph POWER[Power domains]
        P12[12 V actuator rail\nP_GND]
        L5[5 V logic rail\nS_GND]
    end

    PSU --> ESTOP --> P12
    PSU -. input source or local supply .-> BUCK --> L5

    subgraph ACT[Actuator-side loads]
        DRV8871[DRV8871 drivers\nJ1 / J4]
        IBT[IBT-2 / BTS7960 drivers\nJ2 / J3]
        TB6600[TB6600 x2\nJ5 elevator\nsupply voltage pending inspection]
        MOTORS[DC motors + NEMA 23 motors]
    end

    P12 --> DRV8871
    P12 --> IBT
    P12 --> TB6600
    DRV8871 --> MOTORS
    IBT --> MOTORS
    TB6600 --> MOTORS

    subgraph LOGIC[Logic and communication loads]
        RPI[Raspberry Pi 5]
        ESP[ESP32 nodes J1-J5]
        MCP[MCP2515 module\n5 V power]
        CAN[CAN transceivers / telemetry]
    end

    L5 --> RPI
    L5 --> ESP
    L5 --> MCP
    L5 --> CAN

    ESTOP -. logic remains powered .-> L5
```

## Manuscript caption draft

**Figure X. Power-distribution architecture.** The current design separates actuator-side power from the 5 V logic domain. The panic/emergency button is intended to interrupt actuator power while keeping the Raspberry Pi, ESP32 nodes and CAN/telemetry electronics powered for diagnostics. The final TB6600 driver supply voltage and physical grounding/bonding details must be confirmed during the next robot access session.

## Open items before final figure export

- Confirm exact Dell PSU model.
- Confirm supply voltage used by both J5 TB6600 drivers.
- Confirm final `P_GND` / `S_GND` bonding or isolation detail.
- Photograph panic-button wiring path.
- Measure 5 V rail before final logic connection documentation.

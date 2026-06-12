#!/usr/bin/env python3
import struct

class CANMessage:
    """Trama CAN estándar (11-bit ID), payload hasta 8 bytes."""

    def __init__(self, can_id: int, payload: bytes = b''):
        self.can_id  = can_id
        self.payload = payload

    @property
    def dlc(self) -> int:
        return len(self.payload)

    def serialize(self) -> bytes:
        data_padded = self.payload.ljust(8, b'\x00')
        return struct.pack('=IB3x8s', self.can_id, self.dlc, data_padded)

    @classmethod
    def from_bytes(cls, frame: bytes) -> 'CANMessage':
        can_id, dlc, raw = struct.unpack('=IB3x8s', frame)
        return cls(can_id, raw[:dlc])

    def __str__(self) -> str:
        pl = self.payload.hex().upper() or '(sin datos)'
        return f"CANMessage(ID=0x{self.can_id:02X}, DLC={self.dlc}, Payload={pl})"

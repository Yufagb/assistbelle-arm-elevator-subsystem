#!/usr/bin/env python3
import socket, struct
from .message import CANMessage

class CANDriver:
    """SocketCAN RAW."""

    def __init__(self, interface='can0'):
        self.sock = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        self.sock.bind((interface,))
        self.sock.setblocking(False)

    def send(self, msg: CANMessage):
        frame = msg.serialize()
        print(f"Enviando → {msg}")
        self.sock.send(frame)

    def receive(self) -> CANMessage:
        size = struct.calcsize('=IB3x8s')
        frame = self.sock.recv(size)
        msg   = CANMessage.from_bytes(frame)
        print(f"Recibido ← {msg}")
        return msg

    def close(self):
        self.sock.close()

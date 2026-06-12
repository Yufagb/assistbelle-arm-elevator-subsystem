#!/usr/bin/env python3
from can_comm_pkg.driver import CANDriver
from can_comm_pkg.message import CANMessage

def main():
    # Inicializa el driver sobre el bus físico can0
    driver = CANDriver(interface='can0')
    # Construye un mensaje REQUEST_DATA al Motor DC #1 (ID=0x01)
    msg = CANMessage(
        dest_id=0x01,
        flags=CANMessage.FLAGS['REQUEST_DATA'],
        emitter=0x00,
        payload=b''
    )
    # Envía la trama y la imprime
    driver.send(msg)

if __name__ == "__main__":
    main()

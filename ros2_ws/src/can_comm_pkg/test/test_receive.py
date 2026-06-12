#!/usr/bin/env python3
from can_comm_pkg.driver import CANDriver
from time import sleep

def main():
    driver = CANDriver(interface='can0')
    print("Esperando tramas CAN en can0...")
    try:
        while True:
            try:
                msg = driver.receive()
            except BlockingIOError:
                # no hay datos, espera un poco
                sleep(0.1)
    except KeyboardInterrupt:
        print("Finalizando test de recepción.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

from can_comm_pkg.driver import CANDriver
from can_comm_pkg.menu import CLIMenu

def main():
    driver = CANDriver(interface='can0')
    menu   = CLIMenu(driver)
    menu.run()

if __name__ == "__main__":
    main()

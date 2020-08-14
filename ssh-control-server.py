#!/usr/bin/env python3
import argparse
import sys
import os

from ssh_control import SSHControlServer

import logging
from rich.logging import RichHandler
from rich import print

# Rich Logging
FORMAT = "%(message)s"
logging.basicConfig(
            level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

def print_thankyou():
    print("\nThank you for using SSH Control 💖, if you find this project useful then please")
    print("consider to 🌟(star) this project at https://github.com/antony-jr/ssh-control")


print("[bold blue]SSH Control[/bold blue] v0.0.1 (Mk.I), Server Program")
print("Copyright (C) 2020, [bold red]Antony Jr[/bold red].")
print()



application = SSHControlServer()

if __name__ == '__main__':
    application.run()
    print_thankyou()

else:
    if os.getuid() != 0:
        log = logging.getLogger('rich')
        log.warning("Warning you are not running as root, The systemctl command will eventually fail always")

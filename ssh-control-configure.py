#!/usr/bin/env python3
import argparse
import sys

from ssh_control import SSHControlConfigurator

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

if __name__ == '__main__':
    print("[bold magenta]SSH Control[/bold magenta] v0.0.1 (Mk.I), Configuration Program")
    print("Copyright (C) 2020, [bold red]Antony Jr[/bold red].")
    print()


    parser = argparse.ArgumentParser()
    parser.add_argument('ConfigType',help='Either Server or Client')
    args = parser.parse_args()
    SSHControlConfigurator(client=(args.ConfigType.lower() == 'client'))
    print_thankyou()
    sys.exit(0)

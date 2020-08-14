import argparse
import sys
import os

from .SSHControlClient import SSHControlClient 
from .SSHControlServer import SSHControlServer
from .SSHControlConfigurator import SSHControlConfigurator

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



def ExecuteConfigure():
    print("[bold magenta]SSH Control[/bold magenta] v0.0.1 (Mk.I), Configuration Program")
    print("Copyright (C) 2020, [bold red]Antony Jr[/bold red].")
    print()


    parser = argparse.ArgumentParser()
    parser.add_argument('ConfigType',help='Either Server or Client')
    args = parser.parse_args()
    SSHControlConfigurator(client=(args.ConfigType.lower() == 'client'))
    print_thankyou()
    sys.exit(0)

def ExecuteClient():
    print("[bold magenta]SSH Control[/bold magenta] v0.0.1 (Mk.I), Client Program")
    print("Copyright (C) 2020, [bold red]Antony Jr[/bold red].")
    print()

    parser = argparse.ArgumentParser()
    parser.add_argument('host',help='address of ssh-control server')
    parser.add_argument('--verify-host', action='store_true', help='verify if the host is a valid ssh-control Server')
    parser.add_argument('--ssh-on', action='store_true', help='enable SSH Server on Host')
    parser.add_argument('--ssh-off', action='store_true', help='disable SSH Server on Host')
    args = parser.parse_args()


    client = None
    try:
        client = SSHControlClient(args.host)
    except:
        logging.getLogger('rich').error("Cannot construct SSH Control Client")
        print_thankyou()
        sys.exit(-1)

    r_code = 0
    if args.verify_host:
        if not client.verify_host():
            r_code = -1

    elif args.ssh_on:
        if not client.ssh_on():
            r_code = -1

    elif args.ssh_off:
        if not client.ssh_off():
            r_code = -1
        else:
            logging.getLogger('rich').info("No Operation Requested, Exiting")

    print_thankyou()
    sys.exit(r_code)

def Server(environ = None, start_response = None):
    print("[bold blue]SSH Control[/bold blue] v0.0.1 (Mk.I), Server Program")
    print("Copyright (C) 2020, [bold red]Antony Jr[/bold red].")
    print()

    application = SSHControlServer()

    if os.getuid() != 0:
        log = logging.getLogger('rich')
        log.warning("Warning you are not running as root, The systemctl command will eventually fail always")

    return application

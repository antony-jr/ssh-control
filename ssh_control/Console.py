import argparse
import sys
import os

from .SSHControlClient import SSHControlClient 
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
    try:
        SSHControlConfigurator(client=(args.ConfigType.lower() == 'client'))
    except Exception as e:
        logging.getLogger('rich').error("Cannot Configure SSH Control({})".format(e))

    print_thankyou()
    sys.exit(0)

def ExecuteClient():
    print("[bold magenta]SSH Control[/bold magenta] v0.0.1 (Mk.I), Client Program")
    print("Copyright (C) 2020, [bold red]Antony Jr[/bold red].")
    print()

    parser = argparse.ArgumentParser()
    parser.add_argument('--host',help='address of SSH Control server', required=False)
    parser.add_argument('--verify-host', action='store_true', help='verify if the host is a valid ssh-control Server')
    parser.add_argument('--ssh-on', action='store_true', help='enable SSH Server on Host')
    parser.add_argument('--ssh-off', action='store_true', help='disable SSH Server on Host')
    args = parser.parse_args()


    client = None
    try:
        client = SSHControlClient(args.host)
    except Exception as e:
        logging.getLogger('rich').error("Cannot construct SSH Control Client({})".format(e))
        print_thankyou()
        sys.exit(-1)

    r_code = 0
    if args.verify_host:
        if not client.verify_host():
            r_code = -1
        else:
            logging.getLogger('rich').info("Host is a SSH Control Server Instance")

    elif args.ssh_on:
        if not client.ssh_on():
            r_code = -1
        else:
            logging.getLogger('rich').info("SSH is now ON")

    elif args.ssh_off:
        if not client.ssh_off():
            r_code = -1
        else:
            logging.getLogger('rich').info("SSH is now OFF")

    else:
        logging.getLogger('rich').info("No Operation Requested, Exiting")

    if r_code < 0:
        logging.getLogger('rich').error("Cannot complete the requested operation")

    print_thankyou()
    sys.exit(r_code)



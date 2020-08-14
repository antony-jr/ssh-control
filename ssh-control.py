#!/usr/bin/env python3
import argparse
import sys

from ssh_control import SSHControlClient
import logging
from rich.logging import RichHandler
from rich import print

# Rich Logging
FORMAT = "%(message)s"
logging.basicConfig(
            level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)


if __name__ == '__main__':
    print("[bold magenta]SSH Control[/bold magenta] v0.0.1 (Mk.I), Client Program")
    print("Copyright (C) 2020, [bold red]Antony Jr[/bold red].")
    print()


    parser = argparse.ArgumentParser()
    parser.add_argument('host',help='address of ssh-control server')
    parser.add_argument('--verify-host', action='store_true', help='verify if the host is a valid ssh-control Server')
    parser.add_argument('--ssh-on', action='store_true', help='enable SSH Server on Host')
    parser.add_argument('--ssh-off', action='store_true', help='disable SSH Server on Host')
    args = parser.parse_args()

    if args.verify_host != True and args.ssh_on != True and args.ssh_off != True:
        sys.exit(-1)

    client = None
    try:
        client = SSHControlClient(args.host)
    except:
        sys.exit(-1)


    if args.verify_host:
        if not client.verify_host():
            sys.exit(-1)

    elif args.ssh_on:
        if not client.ssh_on():
            sys.exit(-1)

    elif args.ssh_off:
        if not client.ssh_off():
            sys.exit(-1)
    sys.exit(0)

#!/usr/bin/env python3
import argparse
import sys
import os

from ssh_control import SSHControlServer
from ssh_control import SSHControlConfigurator

import logging
from rich.logging import RichHandler

# Rich Logging
FORMAT = "%(message)s"
logging.basicConfig(
            level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--configure', action='store_true', help='Configure ssh-control server')
    args = parser.parse_args()

    if args.configure:
        SSHControlConfigurator()
        sys.exit(0)

application = SSHControlServer()

if __name__ == '__main__':
    application.run()
else:
    if os.getuid() != 0:
        print("Warning you are not running as root, The systemctl command will eventually fail always")


import argparse
import sys

from ssh_control import SSHControlServer
from ssh_control import SSHControlConfigurator

server = SSHControlServer()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--configure', action='store_true', help='Configure ssh-control server')
    args = parser.parse_args()

    if args.configure:
        SSHControlConfigurator()
        sys.exit(0)
    
    server.run();

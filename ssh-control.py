import argparse
import sys

from ssh_control import SSHControlClient


if __name__ == '__main__':
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
        if client.verify_host():
            print("{} is a valid ssh-control server.".format(args.host))
        else:
            print("{} is not a valid ssh-control server.".format(args.host))
    elif args.ssh_on:
        if not client.ssh_on():
            print("Cannot enable SSH on remote, request failed.")
        else:
            print("Request completed successfully.")
    elif args.ssh_off:
        if not client.ssh_off():
            print("Cannot disable SSH on remote, request failed.")
        else:
            print("Request completed successfully.")

    sys.exit(0)

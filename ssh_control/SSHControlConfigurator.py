import configparser
import os

class CannotWriteConfig(Exception):
    def __init__(self):
        self.message = "Cannot write to configuration file, check permissions"

class InvalidInput(Exception):
    def __init__(self):
        self.message = "The given input was invalid"

class SSHControlConfigurator(object):
    def __init__(self, client = False):
        location = lambda x : "{}/.ssh-control-{}.rc".format(os.path.expanduser('~'), x)
        config = configparser.ConfigParser()

        if not client:
            recipient = None
            try:
                recipient = str(input("Please Enter GPG Recipient(Your GPG Key Recipient): "))
            except:
                raise InvalidInput()
                return

            passphrase = None
            try:
                passphrase = str(input("Please Enter Passphrase of your Server's Private GPG Key[This is stored in plain text]: "))
            except:
                raise InvalidInput()
                return
            config['DEFAULT'] = {'GPGRecipient': recipient, 'Passphrase': passphrase}

        else:
            serverRecipient = None
            host = None

            try:
                serverRecipient = str(input("Please Enter Server GPG Recipient: "))
            except:
                raise InvalidInput()
                return

            try:
                host = str(input("Please Enter the host(Only HTTP protocol is supported) for the Server: "))
            except:
                raise InvalidInput()

            if host[len(host)-1] != '/':
                host += '/'

            config['DEFAULT'] = {'ServerGPGRecipient': serverRecipient, 'Host': host}

        X = 'server';
        if client:
            X = 'client';

        try:
            with open(location(X), 'w') as configfile:
                config.write(configfile)
        except:
             raise CannotWriteConfig()
             return



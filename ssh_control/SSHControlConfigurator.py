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
        location = "{}/.ssh-control.rc".format(os.path.expanduser('~'))
        config = configparser.ConfigParser()

        if os.path.exists(location) and os.path.isfile(location):
            config.read(location)

        if not client:
            recipient = None
            try:
                recipient = str(input("Please Enter GPG Recipient: "))
            except:
                raise InvalidInput()
                return

            passphrase = None
            try:
                passphrase = str(input("Please Enter Passphrase of your Private GPG Key[This is stored in plain text]: "))
            except:
                raise InvalidInput()
                return
            config['DEFAULT'] = {'GPGRecipient': recipient, 'Passphrase': passphrase}

        else:
            serverRecipient = None
            try:
                serverRecipient = str(input("Please Enter Server GPG Recipient: "))
            except:
                raise InvalidInput()
                return

            config['DEFAULT'] = {'ServerGPGRecipient': serverRecipient}

        try:
            with open(location, 'w') as configfile:
                config.write(configfile)
        except:
             raise CannotWriteConfig()
             return



import configparser
import os

class CannotWriteConfig(Exception):
    def __init__(self):
        self.message = "Cannot write to configuration file, check permissions"

class InvalidInput(Exception):
    def __init__(self):
        self.message = "The given input was invalid"

class SSHControlConfigurator(object):
    def __init__(self, interactive = True, data = None):
        location = "{}/.ssh-control.rc".format(os.path.expanduser('~'))
        config = configparser.ConfigParser()

        if os.path.exists(location) and os.path.isfile(location):
            config.read(location)

        recipient = None
        try:
            recipient = str(input("Please Enter GPG Recipient: "))
        except:
            raise InvalidInput()
            return

        config['DEFAULT'] = {'GPGRecipient': recipient}

        try:
            with open(location, 'w') as configfile:
                config.write(configfile)
        except:
             raise CannotWriteConfig()
             return



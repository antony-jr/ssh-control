import gnupg
import requests
import json
import os
import configparser

import logging 

class NoRecipient(Exception):
    def __init__(self):
        self.message = "No Server Recipient was given in client configuration."

class CannotGPGEncrypt(Exception):
    def __init__(self):
        self.message = "Cannot do GPG Encryption, Please import your server's Public Key."

class SSHControlClient(object):
    def __init__(self, host):
        self.gpg = gnupg.GPG()
        self.config_file_location = "{}/.ssh-control.rc".format(os.path.expanduser('~'))
        self.configparser = configparser.ConfigParser()

        if os.path.exists(self.config_file_location) and os.path.isfile(self.config_file_location):
            self.configparser.read(self.config_file_location)
        else:
            raise NoRecipient() 
            return;
       
        self.recipient = self.configparser['DEFAULT']['ServerGPGRecipient'];

        # Test GPG Encryption
        test_encrypted = self.gpg.encrypt("SSHControl Test String", self.recipient)
        if not test_encrypted.ok:
            raise CannotGPGEncrypt()

        if host[len(host)-1] != '/':
            host += '/'

        log = logging.getLogger('rich')
        log.info("Set HOST = {}".format(host))

        self.host = host

        # Hopefully, This list will grow in the future.
        self.valid_server_uuid = [
            "f70130bd-c345-4c98-a229-cee3072575bb",
        ]

        

    # Returns True if the host is Running SSH Control Server
    def verify_host(self):
        log = logging.getLogger('rich')

        try:
            response = requests.get(self.host)
        except:
            log.error("Cannot reach host")
            return False

        if response.status_code != 200:
            log.error("Bad Response: {}".format(response.status_code))
            return False

        try:
            json_parsed = json.loads(response.content)
        except:
            log.error("Cannot Parse JSON")
            return False


        try:
            if json_parsed["ssh-control-uuid"] not in self.valid_server_uuid:
                log.error("Invalid SSH Control Server UUID: {}".format(json_parsed['ssh-control-uuid']))
                return False
        except:
            log.error("Cannot Parse JSON")
            return False

        return True

    def ssh_on(self):
        return self._request_server('request-ssh-on')

    def ssh_off(self):
        return self._request_server('request-ssh-off')

    # Returns True if the command executed successfully.
    def _request_server(self, operation):
        log = logging.getLogger('rich')
        if not self.verify_host():
            log.info("HOST is not a valid SSH Control Server")
            return False

        log.info("Sending Operation: {}".format(operation))

        try:
            response = requests.post(self.host + 'request', {"operation": operation})
        except:
            log.error("Failed to acquire request token")
            return False

        if response.status_code != 200:
            log.error("Bad Response Code: {}".format(response.status_code))
            return False

        json_parsed = None
        try:
            json_parsed = json.loads(response.content)
        except:
            log.error("Cannot Parse JSON")
            return False

        head = {"Authorization" : "Bearer {}".format(json_parsed['request_token'])}

        # Now we have to complete the GPG Challenge
        secret = self.gpg.decrypt(str(json_parsed['gpg_encrypted_secret']))

        enc_secret = self.gpg.encrypt(str(secret), self.recipient); # Encrypt using Server Public Key.

        if not enc_secret.ok:
            log.error("Cannot Encrypt using Server's Public Key, Make sure you trust your Server's Public Key")
            return False

        try:
            execute_response = requests.post(self.host + 'execute', data={"secret": "{}".format(str(enc_secret)) }, headers=head)
        except:
            log.error("Failed to execute request token")
            return False

        if execute_response.status_code != 200:
            log.error("Bad Response Code: {}".format(response.status_code))
            return False

        try:
            json_parsed_execute = json.loads(execute_response.content)
        except:
             log.error("Cannot Parse JSON") 
             return False

        log.info(json_parsed_execute)
        if json_parsed_execute['status'] != 'ok':
            log.error(json_parsed_execute['msg'])
            return False 

        log.info("Request Completed Successfully")
        return True

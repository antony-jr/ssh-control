import gnupg
import requests
import json

class SSHControlClient(object):
    def __init__(self, host):
        self.gpg = gnupg.GPG()

        if host[len(host)-1] != '/':
            host += '/'

        self.host = host

        # Hopefully, This list will grow in the future.
        self.valid_server_uuid = [
            "f70130bd-c345-4c98-a229-cee3072575bb",
        ]

    # Returns True if the host is Running SSH Control Server
    def verify_host(self):
        try:
            response = requests.get(host)
        except:
            return False

        if response.status_code != 200:
            return False

        try:
            json_parsed = json.loads(response.content)
        except:
            return False


        try:
            if json_parsed["ssh-control-uuid"] not in self.valid_server_uuid:
                return False
        except:
            return False

    def ssh_on(self):
        return self._request_server('request-ssh-on')

    def ssh_off(self):
        return self._request_server('request-ssh-off')

    # Returns True if the command executed successfully.
    def _request_server(self, operation):
        if not self.verify_host():
            return False

        try:
            response = requests.post(self.host + 'request', {"operation": operation})
        except:
            return False

        json_parsed = None
        try:
            json_parsed = json.loads(response.content)
        except:
            return False

        head = {"Authorization" : "Bearer {}".format(json_parsed['request_token'])}

        # Now we have to complete the GPG Challenge
        secret = self.gpg.decrypt(json_parsed['gpg_encrypted_secret'])

        try:
            execute_response = requests.post(self.host + 'execute', {"secret": "{}".format(secret)}, header=head)
        except:
            return False

        if execute_response.status_code != 200:
            return False

        try:
            json_parsed_execute = json.loads(execute_response)
        except:
            return False

        if json_parsed_execute['status'] != 'ok':
            return False 
        return True

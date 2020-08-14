import gnupg
import configparser
import os
import uuid
import secrets
import datetime
import threading

import subprocess

from flask import Flask

from flask_restful import Api
from flask_restful import Resource, reqparse
from flask_jwt_extended import JWTManager

from flask_jwt_extended import (
        create_access_token,
        jwt_required,
        fresh_jwt_required,
        get_jwt_identity,
)

import logging

# Globals
Lock = threading.Lock()
GPG = gnupg.GPG()
GPGRecipient = None
SecretStore = dict()


class ServerInfo(Resource):
    def get(self):
        log = logging.getLogger('rich')
        log.info("Server Information Requested")
        return {
            "status" : "ok",
            "version": "0.0.1",
            "ssh-control-uuid" : "f70130bd-c345-4c98-a229-cee3072575bb"
        }
 

class Executor(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('secret',
                        type=str,
                        required=True,
                        help="Secret issued by the server which was encrypted by gpg.")

    def __init__(self):
        self.supported_operations = [
                "request-ssh-on",
                "request-ssh-off"
        ]

    @fresh_jwt_required
    def post(self):
        global SecretStore;
        info = get_jwt_identity()
        data = self.parser.parse_args()
        secret = data["secret"]
        
        # If this happens then it is possible that SSH control has
        # been hacked which will never happen but just to 
        # be safe we will issue a warning and log the ip
        if info["operation"] not in self.supported_operations:
            return {
                    "status": "failed",
                    "msg": "Invalid operation in access token, your client and ip are recorded"
            }
 
        # Delete old secrets
        global Lock
        Lock.acquire()
        toDelete = []
        for it in SecretStore:
            elapsed = datetime.datetime.now() - SecretStore[it]['creation']
            if elapsed.total_seconds() >= 60:
                toDelete.append(it)

        for i in toDelete:
            del SecretStore[i]

        if info['operation_uuid'] not in SecretStore:
            Lock.release()
            return {
                    "status": "failed",
                    "msg": "invalid operation uuid"
            }

        actual_secret = SecretStore[info['operation_uuid']]['secret']
        # Delete the secret after access.
        del SecretStore[info['operation_uuid']]
        Lock.release()

        # Verify Secrets
        if str(actual_secret) != str(secret):
            return {
                    "status": "failed",
                    "msg": "authentication failed"
            }

        # Execute the requested operation since the secrets 
        # matched
        command = lambda x : ['systemctl', x , 'sshd']
        try:
            if info['operation'] == 'request-ssh-on':
                process = subprocess.Popen(command('start'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif info['operation'] == 'request-ssh-off':
                process = subprocess.Popen(command('stop'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            return {
                "status": "failed",
                "msg": "Command failed at remote server",
            }

        process.wait()

        return {
                "status": "ok"
        }

class RequestCreator(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('operation',
                        type=str,
                        required=True,
                        help="Operation that need to be executed on SSH Control Server.")

    def __init__(self):
        self.supported_operations = [
                "request-ssh-on",
                "request-ssh-off"
        ]

    def post(self):
        global SecretStore

        data = self.parser.parse_args()
        operation = data["operation"]

        # The operation can be any one of the following,
        # 'request-ssh-on'
        # 'request-ssh-off'

        if operation not in self.supported_operations:
            return {
                "status" : "failed",
                "msg": "invalid operation requested"
            }

        opt_uuid = uuid.uuid4()
        operation_secret = secrets.token_hex(1024) 
    

        global Lock;
        Lock.acquire()
        # Delete old secrets
        toDelete = []
        for it in SecretStore:
            elapsed = datetime.datetime.now() - SecretStore[it]['creation']
            if elapsed.total_seconds() >= 60:
                toDelete.append(it)
        
        for i in toDelete:
            del SecretStore[i]

        SecretStore[str(opt_uuid)] = {
                'secret' : operation_secret,
                'creation': datetime.datetime.now() 
        }
        Lock.release()

        gpg_enc_secret = GPG.encrypt(operation_secret, GPGRecipient)

        info = {
            "operation": operation,
            "operation_uuid": str(opt_uuid),
            "gpg_encrypted_secret" : str(gpg_enc_secret),
        }


        access_tk = create_access_token(identity=info, fresh=True)

        return {
            "status": "ok",
            "request_token": access_tk,
            "gpg_encrypted_secret": str(gpg_enc_secret),
        }


class NoRecipient(Exception):
    def __init__(self):
        self.message = "No Recipient was given in server configuration."

class CannotGPGEncrypt(Exception):
    def __init__(self):
        self.message = "Cannot do GPG Encryption, Please import the required Public Key."

class SSHControlServer(Flask):
    def __init__(self):
        super().__init__("SSH Control Server")

        self.config_file_location = "{}/.ssh-control.rc".format(os.path.expanduser('~'))
        self.configparser = configparser.ConfigParser()

        if os.path.exists(self.config_file_location) and os.path.isfile(self.config_file_location):
            self.configparser.read(self.config_file_location)
        else:
            raise NoRecipient() 
            return;
       
        global GPG
        global GPGRecipient
        GPGRecipient = self.configparser['DEFAULT']['GPGRecipient'];

        # Test GPG Encryption
        test_encrypted = GPG.encrypt("SSHControl Test String", GPGRecipient)
        if not test_encrypted.ok:
            raise CannotGPGEncrypt()


        self.config['JWT_SECRET_KEY'] = secrets.token_hex(4096) # 4096 bytes!
        self.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=1)
        self.config['PROPAGATE_EXCEPTIONS'] = True
        self.api = Api(self)
        self.jwt_manager = JWTManager(self)
        
        self.api.add_resource(ServerInfo, '/');
        self.api.add_resource(RequestCreator, '/request');
        self.api.add_resource(Executor, '/execute');

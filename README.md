# SSH Control

SSH Control is a very simple program (Client and Server) which can switch SSH server ON or OFF depending on the 
received command.

The SSH server is turned ON or OFF only if you complete GPG Challenge.

(i.e)

   * The SSH Control Client can request SSH ON or SSH OFF.

   * When this request is received.
   
   * The SSH Control Server creates a secret hex token of length 1024 bytes(using python secret module).

   * This secret hex token is encrypted with your GPG Public Key.

   * The encrypted message is sent to the client.

   * The client then uses your GPG Private Key to decrypt the secret and send only the decrypted secret to the server.

   * The server then verifies the decrypted secret and then executes your requested operation.

# Instructions

   * Export your Public GPG Key to your Server
   
```
   $ gpg --import your_public_key.asc
```

   * Trust your Public GPG Key Ultimately from your Server's root login.

```
   $ gpg --edit-key "Your Name"

   gpg> trust  # Type it in the gpg shell
   gpg> 5 # To Ultimately trust the key 
   gpg> y # Confirm your choice
   gpg> quit
```

   * Now export your Server's Public GPG Key to your Computer and Also trust it Ultimately.

```
   $ gpg --image your_server_public_key.asc
   $ gpg --edit-key "Your Server Recipient Name"
   
   gpg> trust
   gpg> 5
   gpg> y
   gpg> quit
```

   * Run the configuration script on both server and client

```
   $ ssh-control-configure Server # on your Server
   $ # The GPG Recipient is the name of your Key
   $ # The Required Passphrase is the Server's not your Key
   $ ssh-control-configure Client # on you PC
   $ # The Server GPG Recipient is the name of your Server's Key
```

   * Now Switch on or off your SSH

```
   $ ssh-control https://yourserver.com:9921 --verify-host # To verify everything
   $ ssh-control https://yourserver.com:9921 --ssh-on # To turn on SSH Server
```

   * To Run the SSH Control Server using Gunicorn

```
   $ gunicorn ssh_control # Thats it. 
```

You can also see the ```SSHControl.DebianBuster.service``` to run this as a service in your 
debian server.

# Limitations

   * You will have to put your server's GPG Private Key's passphrase in plain text in your server itself,
     Without that your commands will not work since it will authenticate at the server with a dialog.


I think there is no point in securing your Server's GPG Private Key's passphrase if it is compromised anyway.
**Also you can use a separate GPG Key for SSH Control only.**   


# Installation 

```
   $ pip install git+https://github.com/antony-jr/ssh-control.git
```

# Feedback

I really need a lot of feedback on the security side of this project, So feel free to open a lot of issues.

# License

The MIT License.

Copyright (C) 2020, Antony Jr.

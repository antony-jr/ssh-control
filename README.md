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


# Installation 



# Feedback

I really need a lot of feedback on the security side of this project, So feel free to open a lot of issues.

# License

The MIT License.

Copyright (C) 2020, Antony Jr.

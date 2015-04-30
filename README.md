#Introducing Paramiko

##Effortless ssh programming using python {: .vcenter}

!SLIDE left

##What is Paramiko ?

Paramiko is a Python implementation of the SSHv2 protocol, providing both
client and server functionality.

While it leverages a Python C extension for low level cryptography (PyCrypto),
Paramiko itself is a pure Python interface around SSH networking concepts.

  * Website: http://www.paramiko.org/
  * Souce code: https://github.com/paramiko/paramiko
  * Docs: http://docs.paramiko.org


!SLIDE left

##What can you do with Paramiko ?

Use it to create SSH clients ( `SSHClient` ) to connect to SSHv2 compliant servers

```python

    import paramiko

    # - create the client object
    ssh = paramiko.SSHClient()

    # - you can also choose .AutoAddPolicy() or .RejectPolicy()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())

    # - connect using a `username` and `password`
    ssh.connect('ssh.example.com', username='alice', password='secret')
    
    # or with a key ...
    ssh.connect('ssh.example.com',
                key_filename='/home/steve/.ssh/id_rsa',
                username='alice', password='secret')
    
    # or look for keys under ~/.ssh/ ...
    ssh.connect('ssh.example.com', look_for_keys=True)

    # or connect to local ssh-agent ...
    ssh.connect('ssh.example.com', allow_agent=True)
   
    # - execute a command
    stdin, stdout, stderr = ssh.exec_command("uptime")
    print stdout.read()
```


!SLIDE left

##What else can you do with Paramiko ?

Use it to create SFTP clients

```python

    import paramiko

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    ssh.connect('127.0.0.1', username='alice', password='secret')

    ftp = ssh.open_sftp()
    ftp.get('remotefile.py', 'localfile.py')
    ftp.listdir()
    ftp.close() 
```

!SLIDE left

##What more can you do with Paramiko ?

Use it to create a SSH **Channel** + **Transport** + **Server** (+ optionally, a **Subsystem**)
{: .slide}

In other words an SSH Server
{: .slide}

**Channel** : A secure tunnel across an SSH `Transport`. A Channel is meant to
behave like a socket, and has an API that should be indistinguishable from the
Python socket API. The `secure` part of the socket connection is ensured by
the `Transport`
{: .slide}

**Transport** : An SSH Transport attaches to a stream (usually a socket),
negotiates an encrypted session, authenticates, and then creates stream
tunnels, called `channels`, across the session. A transport object is
created for both the server as well as client ends of a connection.
{: .slide}

**Server** : This implements the server end of the Transport. The interface is
declared by `paramiko.ServerInterface`. This is the actual place where the
Transport looks to authorize channel creation and implement authentication.
{: .slide}

**Subsystem** : A service/command, perhaps external to ssh or built-in
like `sftp`
{: .slide}


!SLIDE left

##How to create a Server ?

Start with the `Channel`, since it is meant to behave like a socket, just use a
socket

```python
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('127.0.0.1', 22))
        sock.listen(100)
        print '[+] Listening for connection ...'
        channel, addr = sock.accept()
    except Exception, e:
        print '[-] Listen/bind/accept failed: ' + str(e)
        sys.exit(1)
    print '[+] Got a connection!'
``` 

!SLIDE left

##How to create a Server ? (cont)

Now, that we have a `Channel` we can use that to create a `Transport`

```python
    transport = paramiko.Transport(channel)
    transport.add_server_key(host_key)
```

and now you can finally tie-in your service...

```python 
    server = Server()
    try:
        transport.start_server(server=server)
    except paramiko.SSHException, x:
        print '[-] SSH negotiation failed.'
``` 

!SLIDE left

##How to create a Server ? (cont)

...or your subsystem. 

```python 
    try:
        transport.set_subsystem_handler(
            'sftp', MyFancySFTPBridge, *stfp_bridge_opts)
        transport.start_server(server=server)
    except paramiko.SSHException, x:
        print '[-] SSH negotiation failed.'
``` 

!SLIDE left

##OK, so what does the `Server` class look like ?

```python 

    class StubServer (paramiko.ServerInterface):

        def check_auth_password(self, username, password):
            # all are allowed
            return AUTH_SUCCESSFUL

        def check_auth_publickey(username, key):
            # all are allowed
            return AUTH_SUCCESSFUL

        def check_channel_request(self, kind, chanid):
            return OPEN_SUCCEEDED
        ...
``` 

!SLIDE left

##What does a `Subsystem` class look like ?

```python 

    class MyFancySFTPBridge (paramiko.SFTPServerInterface):

        def __init__(self, channel, name, server):
            ...

        def start_subsystem(self, name, transport, channel):
            ...
                
        def finish_subsystem(self):
            ...
``` 

!SLIDE left

##How about I show you some real code ? 

On to the demo !

!SLIDE center

##References:

  * A super quick introduction at `http://jessenoller.com/blog/2009/02/05/ssh-programming-with-paramiko-completely-different`
  * Examples taken from the `demos` and `tests` folders in the `paramiko` source tree
  * Another nice little blog post about `paramiko` http://www.minvolai.com/blog/2009/09/How-to-ssh-in-python-using-Paramiko/how-to-ssh-in-python-using-paramiko/
  * Read the API docs and the source code

##Thanks !

####Special thanks to [`pydown`](https://github.com/isnowfy/pydown)



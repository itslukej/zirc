#Internet Relay Chat (IRC) Protocol client library [![Build Status](https://travis-ci.org/itslukej/zirc.svg?branch=master)](https://travis-ci.org/itslukej/zirc)

###Example
```
import zirc, ssl

class Bot(zirc.Client):
    def __init__(self):
        self.connection = zirc.Socket(wrapper=ssl.wrap_socket)
        self.connect(address="irc.freenode.net", 
            port=6697,
            nickname="zirctest",
            ident="bot",
            realname="test bot",
            channels=["##chat"],
            sasl_user="NickServ_Username",
            sasl_pass="NickServ_Password")
        
        self.start()
        
    def on_privmsg(irc, event):
        irc.reply(event, "It works!")

Bot()
```

This library provides a implementation of the IRC protocol, It provides a event-driven IRC Protocol framework.

#Installation

Installing from PyPi:

```
sudo pip install zirc
sudo pip3 install zirc
```

Installing from github:

```
sudo pip install git+https://github.com/itslukej/zirc.git
sudo pip3 install git+https://github.com/itslukej/zirc.git
```

Installing from github will usually have more bug fixes but may contain "bad quality" code.

#Features

- Automatic PING/PONG between the server
- IRC Message parsing
- A simple set up and connection method
- Easy installation

#TODO

- CTCP Support
- Threaded Plugins
- More documentation
- Function arguments like "chan", "nick"


##Using IPv6

To use IPv6 with `zirc.Socket`, you can use the family `socket.AF_INET6`:

```
import socket

self.connection = zirc.Socket(family=socket.AF_INET6)
```

##Ideas

- Multiple connection support

#Contributing

Please discuss code changes that significantly affect client use of the library before merging to the master branch. Please change the version in `setup.py` ahead if the change should be uploaded to PyPi.

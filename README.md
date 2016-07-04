#Internet Relay Chat (IRC) Protocol client library

```
import zirc, ssl

class Bot(zirc.Client):
    def __init__(self):
        self.connection = zirc.Socket(wrapper=ssl.wrap_socket)
        self.connect(address="irc.freenode.net", port=6697, nickname="zirctest", ident="bot", realname="test bot", channels=["#ezzybot"])
        
        self.start()
        
    def on_privmsg(irc, event):
        irc.reply(event, "It works!")

Bot()
```

This library provides a implementation of the IRC protocol, It provides a event-driven IRC Protocol framework.

#Installation

Installing from pypi:

```
sudo pip install zirc
sudo pip3 install zirc
```

Installing from github:

```
sudo pip install git+https://github.com/itslukej/zirc.git
sudo pip3 install git+https://github.com/itslukej/zirc.git
```

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

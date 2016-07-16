#Internet Relay Chat (IRC) Protocol client library [![Build Status](https://travis-ci.org/itslukej/zirc.svg?branch=master)](https://travis-ci.org/itslukej/zirc)

###Quick Start
```python
import zirc, ssl

class Bot(zirc.Client):
    def __init__(self):
        self.connection = zirc.Socket(wrapper=ssl.wrap_socket)
        self.config = zirc.IRCConfig(host="irc.freenode.net", 
            port=6697,
            nickname="zirctest",
            ident="bot",
            realname="test bot",
            channels=["##chat"],
            sasl_user="NickServ_Username",
            sasl_pass="NickServ_Password")
        
        self.connect(self.config)
        self.start()
        
    def on_privmsg(bot, event, irc):
        irc.reply(event, "It works!")
        #Or alternatively:
        #irc.privmsg(event.target, "It works!")

Bot()
```

This library implements IRC protocol, It's an event-driven IRC Protocol framework.

#Installation

####PyPi

```
sudo pip install zirc
sudo pip3 install zirc
```

####Github:

```
sudo pip install git+https://github.com/itslukej/zirc.git
sudo pip3 install git+https://github.com/itslukej/zirc.git
```

> Github will contain latest bug fixes and improvements but sometimes also "bad quality" code.

#Features

- Automatic PING/PONG between the server
- IRC Message parsing
- A simple set up and connection method
- Easy installation
- Easy CTCP Set-up

#IPv6

To use IPv6 with `zirc.Socket`, you can use the family `socket.AF_INET6`:

```python
import socket

self.connection = zirc.Socket(family=socket.AF_INET6)
```

#Proxy

Replace `self.connection`'s attribute `sock` to use a proxy with `zirc.Socket`:

```python
import socks

self.connection = zirc.Socket()
self.connection.sock = socks.socksocket()
self.connection.sock.set_proxy(socks.SOCKS5, "proxy_ip", 1080)
```


#Ideas

- Multiple connection support

#TODO

- More documentation


#Contributing

> Talk to us on #zirc at Freenode

Please discuss code changes that significantly affect client use of the library before merging to the master branch. Change the version in `setup.py` ahead if the change should be uploaded to PyPi.

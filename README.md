# Internet Relay Chat (IRC) Protocol client library
[![Build Status](https://travis-ci.org/itslukej/zirc.svg?branch=master)](https://travis-ci.org/itslukej/zirc)
[![Snippets Stats](https://codebottle.io/embed/search-badge?keywords=zirc&language=4)](https://codebottle.io/?q=zirc)

## Quick Start
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
            caps=zirc.Caps(zirc.Sasl(username="username", password="password")))

        self.connect(self.config)
        self.start()

    def on_privmsg(self, event, irc):
        irc.reply(event, "It works!")
        #Or alternatively:
        #irc.privmsg(event.target, "It works!")

Bot()
```

This library implements the IRC protocol, it's an event-driven IRC Protocol framework.

## Installation

### PyPi

```
sudo pip install zirc
sudo pip3 install zirc
```

### Github

```
sudo pip install git+https://github.com/itslukej/zirc.git
sudo pip3 install git+https://github.com/itslukej/zirc.git
```

> Github will contain the latest bug fixes and improvements but sometimes also "bad quality" code.

## Features

- Automatic PING/PONG between the server
- IRC Message parsing
- A simple set up and connection method
- Easy installation
- Easy CTCP Set-up

### IPv6

To use IPv6 with `zirc.Socket`, you can use the family `socket.AF_INET6`:

```python
import socket

self.connection = zirc.Socket(family=socket.AF_INET6)
```

### Proxy

Initialize `zirc.Socket` with argument `socket_class`:

```python

self.connection = zirc.Socket(socket_class=zirc.Proxy(host="localhost", port=1080, protocol=zirc.SOCKS5))
```

## Examples

You can [find examples for zIRC by me and other users on CodeBottle](https://codebottle.io/?q=%22zirc%22)


## Ideas

- Multiple connection support

## TODO
- More documentation


## Contributing
> Talk to us on #zirc at Freenode

Please discuss code changes that significantly affect client use of the library before merging to the master branch. Change the version in `setup.py` ahead if the change should be uploaded to PyPi.

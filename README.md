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

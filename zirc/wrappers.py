from time import time
from string import Template
from typing import TYPE_CHECKING, Optional, Type
from .util import colors
if TYPE_CHECKING:
    from .event import Event
    from .client import Client

class connection_wrapper(object):
    def __init__(self, irc: Type[Client]):
        self._config = irc._config
        self.send = irc.send
        self.msg = self.privmsg

    # Basic client use
    def privmsg(self, channel: str, message: str, background: Optional[str]=None, rainbow: Optional[bool]=False, style: Optional[str]=None, prefix: Optional[str]=None):
        MSGLEN = 400 - len("PRIVMSG {} :\r\n".format(channel).encode())
        for i in range(0, len(message), MSGLEN):
            msg = Template(message[i:i + MSGLEN]).safe_substitute(**colors.colors)
            if rainbow:
                msg = colors.rainbow(msg)
            if prefix:
                msg = "{0}: {1}".format(prefix, msg)
            self.send("PRIVMSG {0} :{1}".format(channel, colors.stylize(colors.background(msg, background), style)))

    def reply(self, event: Event, message: str, background: Optional[str]=None, rainbow: Optional[bool]=False, style: Optional[str]=None, prefix: Optional[bool]=False):
        if event.target == self._config['nickname']:
            self.privmsg(event.source.nick, message, background=background, rainbow=rainbow, style=style)
        else:
            if prefix:
                self.privmsg(event.target, message, background=background, rainbow=rainbow, style=style, prefix=event.source.nick)
            else:
                self.privmsg(event.target, message, background=background, rainbow=rainbow, style=style)

    def ping(self):
        self.send("PING :{}".format(int(time())))

    def part(self, chan: str):
        self.send("PART {0}".format(chan))

    def nick(self, nick: str):
        self.send("NICK {0}".format(nick))

    def join(self, chan: str, key: Optional[str]=None):
        if key:
            self.send("JOIN {0} {1}".format(chan, key))
        else:
            self.send("JOIN {0}".format(chan))

    def invite(self, chan: str, user: str):
        self.send("INVITE {0} {1}".format(user, chan))

    def action(self, channel: str, message: str):
        self.send("PRIVMSG {0} :\x01ACTION {1}\x01".format(channel, message))

    def kick(self, channel: str, user: str, message: str):
        user = user.replace(" ", "").replace(":", "")
        self.send("KICK {0} {1} :{2}".format(channel, user, message))

    def remove(self, channel: str, user: str, message: str):
        self.send("REMOVE {0} {1} :{2}".format(channel, user, message))

    def op(self, channel: str, nick: str):
        self.send("MODE {0} +o {1}".format(channel, nick))

    def deop(self, channel: str, nick: str):
        self.send("MODE {0} -o {1}".format(channel, nick))

    def ban(self, channel: str, nick: str):
        self.send("MODE {0} +b {1}".format(channel, nick))

    def unban(self, channel: str, nick: str):
        self.send("MODE {0} -b {1}".format(channel, nick))

    def quiet(self, channel: str, nick: str):
        self.send("MODE {0} +q {1}".format(channel, nick))

    def unquiet(self, channel: str, nick: str):
        self.send("MODE {0} -q {1}".format(channel, nick))

    def unvoice(self, channel: str, nick: str):
        self.send("MODE {0} -v {1}".format(channel, nick))

    def voice(self, channel: str, nick: str):
        self.send("MODE {0} +v {1}".format(channel, nick))

    def mode(self, channel: str, nick: str, mode: str):
        self.send("MODE {0} {1} {2}".format(channel, mode, nick))

    def notice(self, user: str, message: str):
        self.send("NOTICE {0} :{1}".format(user, message))

    def quit(self, message: Optional[str]=""):
        self.send("QUIT :{0}".format(message))

    def ctcp(self, user: str, message: str):
        self.send("PRIVMSG {0} :\x01{1}\x01\x01".format(user, message))

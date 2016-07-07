import six
import os, json

irc_events = json.load(open(os.path.join(os.path.dirname(__file__), "resources", "events.json"), "r"))

class Event(object):

    def __init__(self, raw):
        self.raw = ''.join([i if ord(i) < 128 else ' ' for i in raw])
        if raw.startswith(":"):
            raw = raw.replace(":", "", 1)
            if len(raw.split(" ", 3)) > 3:
                self.source, self.type, self.target, args = raw.split(" ", 3)
            else:
                self.source, self.type, self.target = raw.split(" ", 3)
                args = ""
            self.source = NickMask(self.source)
        else:
            self.type, args = raw.split(" ", 1)
            self.source = self.target = None
        self.arguments = []
        args = args.split(":", 1)
        for arg in args[0].split(" "):
            if len(arg) > 0:
                self.arguments.append(arg)
        if len(args) > 1:
            self.arguments.append(args[1])
    
        self.text_type = irc_events.get(self.type, self.type).upper()

    def __str__(self):
        tmpl = (
            "type: {type}, "
            "text_type: {text_type}, "
            "source: {source}, "
            "target: {target}, "
            "arguments: {arguments}, "
            "raw: {raw} "
        )
        return tmpl.format(**vars(self))
    __repr__ = __str__

class NickMask(six.text_type):
    @classmethod
    def from_params(cls, nick, user, host):
        return cls('{nick}!{user}@{host}'.format(**vars()))

    @property
    def nick(self):
        nick, sep, userhost = self.partition("!")
        return nick

    @property
    def userhost(self):
        nick, sep, userhost = self.partition("!")
        return userhost or None

    @property
    def host(self):
        nick, sep, userhost = self.partition("!")
        user, sep, host = userhost.partition('@')
        return host or None

    @property
    def user(self):
        nick, sep, userhost = self.partition("!")
        user, sep, host = userhost.partition('@')
        return user or None

    @classmethod
    def from_group(cls, group):
        return cls(group) if group else None
import os, json
from typing import Any, Dict, List, Optional, Union

with open(os.path.join(os.path.dirname(__file__), "resources", "events.json"), "r") as f:
    irc_events: Dict[str, str] = json.load(f)

class NickMask(str):
    @classmethod
    def from_params(cls, nick: str, user: str, host: str):
        return cls('{nick}!{user}@{host}'.format(nick, user, host))

    @property
    def nick(self):
        nick = self.partition("!")[0]
        return nick

    @property
    def userhost(self):
        userhost = self.partition("!")[2]
        return userhost or None

    @property
    def host(self):
        userhost = self.partition("!")[2]
        host = userhost.partition('@')[2]
        return host or None

    @property
    def user(self):
        userhost = self.partition("!")[2]
        user = userhost.partition('@')[0]
        return user or None

    @classmethod
    def from_group(cls, group: Optional[Any]):
        return cls(group) if group else None


class Event(object):

    def __init__(self, raw: str):
        self.raw = ''.join([i if ord(i) < 128 else ' ' for i in raw])
        self.source: Optional[NickMask] = None
        self.type: str = None
        self.target: str = None
        self.arguments: List[str] = []
        self.tags: List[Union[str, Dict[str, str]]] = []
        args = ""
        args1 = ""
        if raw.startswith("@"):
            tags, raw = raw.split(" ", 1)
            tags = tags.replace("@", "", 1)
            tags = tags.split(";")
            for tag in tags:
                if "=" in tag:
                    tag = tag.split("=", 1)
                    self.tags.append({tag[0]: tag[1]})
                else:
                    self.tags.append(tag)
        if " :" in raw:
            raw, args1 = raw.split(" :", 1)
        if raw.startswith(":"):
            raw = raw.replace(":", "", 1)
            raw = raw.split(" ")
            self.source = raw[0]
            self.type = raw[1]
            if len(raw) > 2 and not self.type == "ACCOUNT":
                self.target = raw[2]
            if len(raw) > 3:
                args = " ".join(raw[3:])
            if self.type == "ACCOUNT":
                args = raw[2]
            self.source = NickMask(self.source)
        else:
            raw = raw.split(" ")
            self.type = raw[0]
            if len(raw) > 1:
                args = " ".join(raw[1:])
        if len(args1) > 0:
            if len(args) > 0:
                args = "{0} :{1}".format(args, args1)
            else:
                args = ":{0}".format(args1)
        if args.startswith(":"):
            args = args.split(":", 1)
        else:
            args = args.split(" :", 1)
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
            "tags: {tags}, "
            "raw: {raw} "
        )
        return tmpl.format(**vars(self))
    __repr__ = __str__

from typing import Any, Callable, List, Optional, Type, TypedDict, Union
from .caps import Caps

class IRCConfigDict(TypedDict):
    host: str
    port: int
    nickname: str
    ident: str
    realname: str
    channels: List[str]
    caps: Type[Caps]

class IRCConfig(object):
    """
    Class for holding zIRC config infomation.

    >>> self.config = zirc.IRCConfig(nickname="IRCConfigTest")
    >>> self.connect(self.config)
    """
    def __init__(self, **c):
        self.dict: IRCConfigDict = {
                        "host": "irc.freenode.net",
                        "port": 6667,
                        "nickname": "my-zIRC-Bot",
                        "ident": "bot",
                        "realname": "zIRC Bot",
                        "channels": ["#zirc"],
                        "caps": Caps()
                     }
        self.dict.update(c)

    def sterilise(self, method: Callable[[IRCConfigDict], Type[IRCConfigDict]]):
        return method(self.dict)

    def __getitem__(self, key: str) -> Union[str, int, Caps, list[str]]:
        return self.dict[key]

    def __setitem__(self, key: str, value: Union[str, int, Caps, list[str]]):
        self.dict[key] = value

    def get(self, key: str, default: Optional[Any]=None) -> Union[str, int, Caps, list[str]]:
        return self.dict.get(key, default)

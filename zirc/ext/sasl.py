# SASL authentication for zirc

import base64
from typing import List, Literal, Optional, TYPE_CHECKING, Type, Union
from .caps import BaseCaps
from ..errors import SASLError
if TYPE_CHECKING:
    from ..client import Client
    from ..event import Event


class Sasl(BaseCaps):
    name = "sasl"

    def __init__(self, username: str, password: str, method: Optional[str]="plain"):
        self.username = username
        self.password = password
        self.method: Literal['plain', 'external'] = method
        self.retries: int = 0

    def run(self, bot: Type[Client], args: Optional[List[str]]=None):
        if args is None:
            mechanisms = ["EXTERNAL", "PLAIN"]
        else:
            mechanisms = args
        self.bot = bot
        bot.listen(self.on_authenticate, "authenticate")
        bot.listen(self.on_saslfailed, "saslfailed")
        bot.listen(self.on_saslsuccess, "saslsuccess")
        if self.method.upper() in mechanisms:
            if self.method in ["plain", "external"]:
                bot.send("AUTHENTICATE " + self.method.upper())
            else:
                raise SASLError("Not implemented yet")
        else:
            raise SASLError("Not supported by server")

    def on_authenticate(self, event: Event):
        if event.arguments[0] == "+":
            if self.method == 'plain':
                password = base64.b64encode("{0}\x00{0}\x00{1}".format(self.username, self.password).encode("UTF-8")).decode("UTF-8")
            elif self.method == 'external':
                password = "+"
            self.bot.send("AUTHENTICATE {0}".format(password))

    def on_saslfailed(self, event: Event):
        self.retries += 1
        if self.method == 'external':
            if self.retries == 2:
                self.retries = 1
                self.method = 'plain'
                self.bot.send("AUTHENTICATE PLAIN")
            else:
                self.bot.send("AUTHENTICATE EXTERNAL")
        elif self.method == 'plain':
            if not self.retries == 2:
                self.bot.send("AUTHENTICATE PLAIN")
            else:
                self.bot.send("AUTHENTICATE *")
                raise SASLError("SASL authentication failed!")

    def on_saslsuccess(self, event: Event):
        self.bot.send("CAP END")

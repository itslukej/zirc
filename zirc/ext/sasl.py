# SASL authentication for zirc

import base64
from ..errors import SASLError

class Sasl(object):
    name = "sasl"

    def __init__(self, username, password, method="plain"):
        self.username = username
        self.password = password
        self.method = method
        self.retries = 0

    def run(self, bot, args=None):
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

    def on_authenticate(self, event):
        if event.arguments[0] == "+":
            if self.method == 'plain':
                password = base64.b64encode("{0}\x00{0}\x00{1}".format(self.username, self.password).encode("UTF-8")).decode("UTF-8")
            elif self.method == 'external':
                password = base64.b64encode(self.username.encode("UTF-8")).decode("UTF-8")
            self.bot.send("AUTHENTICATE {0}".format(password))

    def on_saslfailed(self, event):
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
                raise SASLError("SASL authentication failed!")

    def on_saslsuccess(self, event):
        self.bot.send("CAP END")

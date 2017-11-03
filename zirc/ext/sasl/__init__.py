# SASL authentication for zirc

import base64
from . import scram
from ...errors import SASLError

class Sasl(object):
    name = "sasl"

    def __init__(self, username, password, method="plain"):
        self.username = username
        self.password = password
        self.method = method
        self.retries = 0
        self.sasl_scram_state = {'step': 'uninitialized'}

    def run(self, bot, args=None):
        if args is None:
            mechanisms = ["SCRAM-SHA256-PLUS", "SCRAM-SHA256", "EXTERNAL", "PLAIN"]
        else:
            mechanisms = args
        self.bot = bot
        bot.listen(self.on_authenticate, "authenticate")
        bot.listen(self.on_saslfailed, "saslfailed")
        bot.listen(self.on_saslsuccess, "saslsuccess")
        if self.method.upper() in mechanisms:
            if self.method.startswith("scram-"):
                step = self.sasl_scram_state['step']
                try:
                    if step == 'uninitialized':
                        scram.doAuthenticateScramFirst(self, method)
                    elif step == 'first-sent':
                        scram.doAuthenticateScramChallenge(self, string)
                    elif step == 'final-sent':
                        scram.doAuthenticateScramFinish(self, string)
                    else:
                        assert False
                except scram.ScramException:
                    bot.send('AUTHENTICATE *')
                    self.retries +=  2
            elif self.method in ["plain", "external"]:
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
                password = "+"
            self.bot.send("AUTHENTICATE {0}".format(password))

    def on_saslfailed(self, event):
        self.retries += 1
        if self.method == 'external':
            if self.retries >= 2:
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

    def on_saslsuccess(self, event):
        self.bot.send("CAP END")

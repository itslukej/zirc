# SASL authentication for zirc

import base64
from ..errors import SASLError

class Sasl(object):
    name = "sasl"
    def __init__(self, username, password, method="plain"):
        self.username = username
        self.password = password
        self.method = method
    def run(self, bot):
        self.bot = bot
        bot.listen(self.on_authenticate,"authenticate")
        bot.listen(self.on_saslfailed,"saslfailed")
        bot.listen(self.on_saslsuccess,"saslsuccess")
        if self.method == "plain":
            bot.send("AUTHENTICATE PLAIN")
        else:
            raise SASLError("not implemented yet")
    
    def on_authenticate(self,event):
        if event.arguments[0] == "+":
            password = base64.b64encode("{0}\x00{0}\x00{1}".format(self.username, self.password).encode("UTF-8")).decode("UTF-8")
            self.bot.send("AUTHENTICATE {0}".format(password))

    def on_saslfailed(self, event):
        raise SASLError("SASL authentication failed!") # do something else later, like try another method

    def on_saslsuccess(self, event):
        self.bot.send("CAP END")

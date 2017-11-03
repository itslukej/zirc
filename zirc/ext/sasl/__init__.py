# SASL authentication for zirc

import base64
import pyxmpp2_scram as scram
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
                        hash_name = self.method[len('scram-'):]
                        if hash_name.endswith('-plus'):
                            hash_name = hash_name[:-len('-plus')]
                        hash_name = hash_name.upper()
                        if hash_name not in scram.HASH_FACTORIES:
                            self.retries += 2
                            return
                        authenticator = scram.SCRAMClientAuthenticator(hash_name, channel_binding=False)
                        self.sasl_scram_state['authenticator'] = authenticator
                        client_first = authenticator.start({
                            'username': self.username,
                            'password': self.password,
                         })
                        self.sendSaslString(client_first)
                        self.sasl_scram_state['step'] = 'first-sent'
                    elif step == 'first-sent':
                        client_final = self.sasl_scram_state['authenticator'].challenge(challenge)
                        self.sendSaslString(client_final)
                        self.sasl_scram_state['step'] = 'final-sent'
                    elif step == 'final-sent':
                        try:
                            res = self.sasl_scram_state['authenticator'].finish(data)
                        except scram.BadSuccessException:
                            self.retries += 2
                        else:
                            self.sasl_scram_state['step'] = 'authenticated'
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

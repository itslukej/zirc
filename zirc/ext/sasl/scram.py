import pyxmpp2_scram as scram

def doAuthenticateScramFirst(self, mechanism):
    """Handle sending the client-first message of SCRAM auth."""
    hash_name = mechanism[len('scram-'):]
    if hash_name.endswith('-plus'):
        hash_name = hash_name[:-len('-plus')]
    hash_name = hash_name.upper()
    if hash_name not in scram.HASH_FACTORIES:
        self.retries += 2
        return
    authenticator = scram.SCRAMClientAuthenticator(hash_name, channel_binding=False)
    self.sasl_scram_state['authenticator'] = authenticator
    client_first = authenticator.start({
        'username': self.sasl_username,
        'password': self.sasl_password,
        })
    self.bot.send("AUTHENTICATE {0}".format(client_first))
    self.sasl_scram_state['step'] = 'first-sent'

def doAuthenticateScramChallenge(self, challenge):
    client_final = self.sasl_scram_state['authenticator'].challenge(challenge)
    self.bot.send("AUTHENTICATE {0}".format(client_final))
    self.sasl_scram_state['step'] = 'final-sent'

def doAuthenticateScramFinish(self, data):
    try:
        res = self.sasl_scram_state['authenticator'].finish(data)
    except scram.BadSuccessException:
        self.retries += 2
    else:
        self.sasl_scram_state['step'] = 'authenticated'
        self.bot.send("AUTHENTICATE +")

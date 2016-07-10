class connection_wrapper(object):
    def __init__(self, irc):
        self.send = irc.send
        self.reply = irc.reply
        self.msg = irc.privmsg
        self.privmsg = irc.privmsg
    def ping(self):
        self.send("PING :{}".format(str(int(time()))).encode('utf-8'))

    def part(self, chan):
        self.send("PART {0}".format(chan))

    def nick(self, nick):
        self.send("NICK {0}".format(nick))

    def join(self, chan):
        self.send("JOIN {0}".format(chan))

    def invite(self, chan, user):
        self.send("INVITE {0} {1}".format(user, chan))

    def action(self, channel, message):
        self.sendmsg(channel,"\x01ACTION " + message + "\x01")

    def kick(self,channel, user, message):
        user = user.replace(" ","").replace(":","")
        self.send("KICK " + channel + " " + user+ " :" + message)

    def op(self, channel, nick):
        self.send("MODE {0} +o {1}".format(channel, nick))

    def deop(self, channel, nick):
        self.send("MODE {0} -o {1}".format(channel, nick))

    def ban(self, channel, nick):
        self.send("MODE {0} +b {1}".format(channel, nick))

    def unban(self, channel, nick):
        self.send("MODE {0} -b {1}".format(channel, nick))

    def quiet(self, channel, nick):
        self.send("MODE {0} +q {1}".format(channel, nick))

    def unquiet(self, channel, nick):
        self.send("MODE {0} -q {1}".format(channel, nick))

    def unvoice(self, channel, nick):
        self.send("MODE {0} -v {1}".format(channel, nick))

    def voice(self, channel, nick):
        self.send("MODE {0} +v {1}".format(channel, nick))

    def mode(self, channel, nick, mode):
        self.send("MODE {0} {1} {2}".format(channel, mode, nick))
        
    def notice(self, user, message):
        self.send("NOTICE {0} :{1}".format(user, message))

    def quit(self, message=""):
        self.send("QUIT :"+message)
    
    def ctcp(self, user, message):
        self.send("PRIVMSG {0} :\x01{1}\x01\x01".format(user, message))
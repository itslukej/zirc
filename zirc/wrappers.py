from time import time

class connection_wrapper(object):
    def __init__(self, irc):
        self.send = irc.send
        self.reply = irc.reply
        self.msg = irc.privmsg
        self.privmsg = irc.privmsg

    def ping(self):
        """Send a PING to the connected server"""
        self.send("PING :{0}".format(int(time())))

    def part(self, chan):
        """Part a specified channel"""
        self.send("PART {0}".format(chan))

    def nick(self, nick):
        """Change nickname to the one specified"""
        self.send("NICK {0}".format(nick))

    def join(self, chan, key=None):
        """<channel> [<key>]
        Joins specified channel"""
        if key:
            self.send("JOIN {0} {1}".format(chan, key))
        else:
            self.send("JOIN {0}".format(chan))

    def invite(self, chan, user):
        """Invite user to a channel"""
        self.send("INVITE {0} {1}".format(user, chan))

    def action(self, channel, message):
        self.send("PRIVMSG {0} :\x01ACTION {1}\x01".format(channel, message))

    def kick(self, channel, user, message):
        user = user.replace(" ", "").replace(":", "")
        self.send("KICK {0} {1} :{2}".format(channel, user, message))

    def remove(self, channel, user, message):
        self.send("REMOVE {0} {1} :{2}".format(channel, user, message))

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
        self.send("MODE {0} {1} {2}".format(channel, nick, mode))

    def notice(self, user, message):
        self.send("NOTICE {0} :{1}".format(user, message))

    def quit(self, message=""):
        self.send("QUIT :{0}".format(message))

    def ctcp(self, user, message):
        self.send("PRIVMSG {0} :\x01{1}\x01\x01".format(user, message))

class Database(dict):
    """Holds a dict that contains all the information about the users in a channel"""
    def __init__(self, irc):
        self.irc = irc

    def remove_entry(self, event, nick):
        try:
            del self[event.target][nick]
        except KeyError:
            for i in self[event.target].values():
                if i['host'] == event.source.host:
                    del self[event.target][i['hostmask'].split("!")[0]]
                    break

    def add_entry(self, channel, nick, hostmask, account):
        self[channel][nick] = {
            'hostmask': hostmask,
            'host': hostmask.split("@")[1],
            'account': account,
            'seen': []
        }

    def get_user_host(self, channel, nick):
        try:
            host = "*!*@" + self[channel][nick]['host']
        except KeyError:
            self.irc.send("WHO {0} nuhs%nhuac".format(channel))
            host = "*!*@" + self[channel][nick]['host']
        return host
  

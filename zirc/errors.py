import sys
if sys.version_info > (2,7):
    class ConnectionError(OSError):
        pass

class IRCError(ConnectionError):
    pass

class SASLError(IRCError):
    pass
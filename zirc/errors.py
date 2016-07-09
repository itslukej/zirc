import sys as _sys
if _sys.version_info > (2,7):
    class ConnectionError(OSError):
        pass

class IRCError(ConnectionError):
    pass

class SASLError(IRCError):
    pass

class NoSocket(IRCError):
    pass
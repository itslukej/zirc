import sys as _sys
if _sys.version_info >= (2, 7, 0) and _sys.version_info < (3, 3):
    class ConnectionError(OSError):
        pass

class IRCError(ConnectionError):
    pass

class SASLError(IRCError):
    pass

class NoSocket(IRCError):
    pass

class NoConfig(IRCError):
    pass


# test.py
class TestError(Exception):
    pass

class InvalidLine(TestError):
    pass

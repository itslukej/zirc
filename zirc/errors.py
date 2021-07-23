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

class DependencyError(Warning):
    pass

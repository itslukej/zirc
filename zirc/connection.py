import socket

same = lambda x: x

class Socket(object):
    """
    A class for creating socket connections.
    
    Creating a connection:
        address = ("irc.stuxnet.xyz", 6697)
        Socket(wrapper=ssl.wrap_socket, family=socket.AF_INET6)(address)
    """
    def __init__(self, wrapper=same, family=socket.AF_INET, bind_address=None):
        self.sock = socket.socket(family, socket.SOCK_STREAM)
        self.bind_address = bind_address
        self.wrapper = wrapper
    def connect(self, socket_address):
        self.sock = self.wrapper(self.sock)
        self.bind_address and sock.bind(self.bind_address)
        self.sock.connect(socket_address)
        
        return self.sock
    __call__ = connect
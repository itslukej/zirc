import socket
try:
    import socks
    SOCKS5 = socks.SOCKS5
    SOCKS4 = socks.SOCKS4
    HTTP = socks.HTTP

    class Proxy(socks.socksocket):
        def __init__(self, host: str="localhost", port:int=1080, protocol=socks.SOCKS5):
            self.host = host
            self.port = port
            self.protocol = protocol

        def __repr__(self):
            return "Proxy({0}, {1})".format(self.host, self.protocol)

        def __call__(self, family: socket.AddressFamily=socket.AF_INET, type:socket.SocketKind=socket.SOCK_STREAM):
            super(Proxy, self).__init__(family, type)
            self.set_proxy(self.protocol, self.host, self.port)
            return self
except ImportError:
    from .. import errors
    def x(*args, **kwargs):
        raise errors.DependencyError('To use proxy features with zIRC, we require that PySocks be installed')
    SOCKS5 = SOCKS4 = HTTP = Proxy = x

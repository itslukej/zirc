import socket
try:
    import socks
    SOCKS5 = socks.SOCKS5
    SOCKS4 = socks.SOCKS4
    HTTP = socks.HTTP

    class Proxy(socks.socksocket):
        def __init__(self, host="localhost", port=1080, protocol=socks.SOCKS5):
            self.host = host
            self.port = port
            self.protocol = protocol

        def __repr__(self):
            return "Proxy({0}, {1})".format(self.host, self.protocol)

        def __call__(self, family=socket.AF_INET, type=socket.SOCK_STREAM):
            super(Proxy, self).__init__(family, type)
            self.set_proxy(self.protocol, self.host, self.port)
            return self
except ImportError:
    raise ImportError('To use proxy features with zIRC, we require that PySocks be installed')

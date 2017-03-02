from .client import Client
from .connection import Socket
from .config import IRCConfig
from .ext.sasl import Sasl
try:
    from .ext.proxy import SOCKS4, SOCKS5, HTTP, Proxy
except ImportError:
    pass
from .ext.fifo import Fifo
from .caps import Caps
__version__ = '1.2.8'

from __future__ import annotations
from typing import TYPE_CHECKING, Type
if TYPE_CHECKING:
    from zirc.client import Client


class BaseCaps(object):
    name = ""
    def run(self, bot: Type[Client]):
        pass

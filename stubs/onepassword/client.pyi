from .core import InnerClient as InnerClient, UniffiCore as UniffiCore
from .defaults import DesktopAuth as DesktopAuth, new_default_config as new_default_config
from .desktop_core import DesktopCore as DesktopCore
from .groups import Groups as Groups
from .items import Items as Items
from .secrets import Secrets as Secrets
from .vaults import Vaults as Vaults

class Client:
    secrets: Secrets
    items: Items
    vaults: Vaults
    groups: Groups
    @classmethod
    async def authenticate(cls, auth: str | DesktopAuth, integration_name: str, integration_version: str) -> Client: ...

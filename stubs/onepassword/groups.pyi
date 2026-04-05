from .core import InnerClient as InnerClient
from .types import Group as Group, GroupGetParams as GroupGetParams
from _typeshed import Incomplete

class Groups:
    inner_client: Incomplete
    def __init__(self, inner_client: InnerClient) -> None: ...
    async def get(self, group_id: str, group_params: GroupGetParams) -> Group: ...

from _typeshed import Incomplete

class DesktopSessionExpiredException(Exception):
    message: Incomplete
    def __init__(self, message) -> None: ...

class RateLimitExceededException(Exception):
    message: Incomplete
    def __init__(self, message) -> None: ...

def raise_typed_exception(e: Exception): ...

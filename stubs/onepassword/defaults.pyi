from _typeshed import Incomplete
from onepassword.build_number import SDK_BUILD_NUMBER as SDK_BUILD_NUMBER

SDK_LANGUAGE: str
SDK_VERSION = SDK_BUILD_NUMBER
DEFAULT_INTEGRATION_NAME: str
DEFAULT_INTEGRATION_VERSION: str
DEFAULT_REQUEST_LIBRARY: str
DEFAULT_REQUEST_LIBRARY_VERSION: str
DEFAULT_OS_VERSION: str

class DesktopAuth:
    account_name: Incomplete
    def __init__(self, account_name: str) -> None: ...

def new_default_config(auth: DesktopAuth | str, integration_name, integration_version): ...

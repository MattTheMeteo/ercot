from onepassword.client import Client
from os import getenv

async def get_onepass_secret(secret: str) -> str:
    """Taken from 1Pass API example: https://github.com/1Password/onepassword-sdk-python?tab=readme-ov-file#requirements
    This function will return the given secret from the given vault, provided permissions 
    (the SERVICE_ACCOUNT_TOKEN) is set up correctly.

    Args:
        secret (str): the secret reference to the 1Password secret

    Returns:
        str: the secret from the Green Shoots vault
    """
    token = getenv("OP_SERVICE_ACCOUNT_TOKEN")
    client = await Client.authenticate(token, integration_name="Green Shoots", integration_version="0.1")
    value = await client.secrets.resolve(secret_reference=secret)
    return value
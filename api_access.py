# ERCOT has API access through their new Public Data API
import logging
import polars as pl
from typing import Optional
from utils import get_onepass_secret
import httpx

logging.basicConfig(level=logging.INFO)

async def get_ercot_pub_token():
    """The ERCOT API needs a token to be refreshed each hour. This function will handle that.
    Docs: https://developer.ercot.com/applications/pubapi/user-guide/registration-and-authentication/#__tabbed_1_5
    Returns:
        _type_: _description_
    """
    # From ERCOT's Developer Portal
    logging.info("Grabbing 1Password values")
    try:
        user = await get_onepass_secret("op://Green Shoots/ERCOT Public API/username")
        pasw = await get_onepass_secret("op://Green Shoots/Ercotb2c/password")
    except Exception as e:
        logging.error(f"Failed to retrieve credentials: {e}")
    # Authorization URL - /shrug
    url = (
        "https://ercotb2c.b2clogin.com/ercotb2c.onmicrosoft.com/B2C_1_PUBAPI-ROPC-FLOW/oauth2/v2.0/token"
        f"?username={user}&password={pasw}&grant_type=password"
        "&scope=openid+fec253ea-0d06-4272-a5e6-b478baeecd70+offline_access"
        "&client_id=fec253ea-0d06-4272-a5e6-b478baeecd70&response_type=id_token"
    )
    # Post the token
    resp = httpx.post(url=url)
    if resp.status_code != 200:
        raise Exception(f"Failed to get the ERCOT Public API token: {resp.status_code}")
    # Get the token
    token = resp.json().get("access_token")
    return token


async def format_ercot_pub_header(
    token: Optional[str] = None, key: Optional[str] = None
):
    """Given some inputs, just return the formatted header we need to make requests to ERCOT.
    Defaults to the token and key we get from the 1Password vault.

    Args:
        token (string, optional): Defaults to get_ercot_pub_token().
        key (string, optional): Defaults to asyncio.run(get_onepass_secret("op://Green Shoots/ERCOT Public API/credential")).
    """
    token = token or await get_ercot_pub_token()
    key = key or await get_onepass_secret(
        "op://Green Shoots/ERCOT Public API/credential"
    )
    header = {"Authorization": f"Bearer {token}", "Ocp-Apim-Subscription-Key": key}
    return header


class ERCOTRequest:
    """Simple lil class that helps keep ERCOT methods together."""

    def __init__(self, endpoint: str, params: dict):   
        self.endpoint = endpoint
        self.params = params

    def _get_ercot_pub_base_url(self):
        return "https://api.ercot.com/api/public-reports"

    def _get_ercot_pub_version(self):
        httpx.get(f"{self._get_ercot_pub_base_url()}/version")

    def build_ercot_url(self):
        """Given an endpoint, build the full URL to make a request to ERCOT.
        Args:
            endpoint (string): The ERCOT dataset to hit
        """
        return f"{self._get_ercot_pub_base_url()}/{self.endpoint}"

    def _get_number_of_pages(self, response: httpx.Response) -> int:
        """Given a response from the ERCOT API, return the number of pages in the response.
        Args:
            response (httpx.Response): The response from the ERCOT API
        Returns:
            int: The number of pages in the response
        """
        # We're reading the whole thing but like - whatever. Maybe in the future we can just get the pagination info.
        df = pl.read_json(response.content)
        return df.unnest("_meta").select(pl.col("totalPages")).item()

    def _unpack_ercot_response(self, response: httpx.Response) -> pl.DataFrame:
        """Given a response from the ERCOT API, unpack it into a Polars DataFrame.
        My hope is to use this across a number of different datasets.
        Args:
            response (httpx.Response): The response from the ERCOT API
        Returns:
            a polars DataFrame object containing the data.
        """
        # Return the schema of the data
        df = pl.read_json(response.content)
        nms = (
            df.select(pl.col("fields"))
            .explode("fields")
            .unnest("fields")["name"]
            .to_list()
        )
        # Let's unpack the data itself
        exp = (
            df.select(pl.col("data"))
            .explode("data")
            .select(pl.col("data").list.to_struct(fields=nms))
            .unnest("data")
        )
        return exp

    async def fetch_ercot_data(self) -> pl.DataFrame:
        """Given a URL and some parameters, fetch the data from ERCOT.

        Args:
            url (str): this is going to be the URL for the dataset
            params (dict): extra parameters to pass to the

        Returns:
            pl.DataFrame: it's got the data in it, hopefully
        """
        # Hard code some params for now
        # Test if we need anything besides the emilID
        # url = self.build_ercot_url(endpoint="np4-190-cd/dam_stlmnt_pnt_prices")
        
        # TODO - pagination
        url = self.build_ercot_url()
        headers = await format_ercot_pub_header()
        params = self.params
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            pages = self._get_number_of_pages(resp)
            df = self._unpack_ercot_response(resp)
            logging.info(f"Found {pages} pages in the response")
            if pages == 1:
                return df
            else:
                hold = []
                for page in range(2, pages):
                    params["page"] = page
                    resp = await client.get(url, headers=headers, params=params, timeout=10)
                    hold.append(self._unpack_ercot_response(resp))
                out = pl.concat([df, *hold])
                return out

import asyncio
from typing import Any

import polars as pl

from api_access import ERCOTRequest, process_np_190_data

params: dict[str, Any] = {
    "deliveryDateFrom": "2025-03-01",
    "deliveryDateTo": "2025-03-18",
    "settlementPoint": "HB_HOUSTON",
    "page": 1,
}


def main(params: dict[str, Any]) -> pl.DataFrame:
    req: ERCOTRequest = ERCOTRequest(
        endpoint="np4-190-cd/dam_stlmnt_pnt_prices", params=params
    )
    out: pl.DataFrame = asyncio.run(req.fetch_ercot_data())
    out = process_np_190_data(out)
    out.write_csv(
        file=f"/home/mlivingston/gs_data/{params['settlementPoint']}_ERCOT_DA.csv"
    )
    return out


if __name__ == "__main__":
    main(params)

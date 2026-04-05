import argparse
import asyncio
import logging

import polars as pl

from api_access import ERCOTRequest, process_np_190_data
from db_access import get_location_id, upsert_price_data, upsert_price_locations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def fetch_and_store_dam(
    from_date: str,
    to_date: str,
    settlement_point: str = "HB_HOUSTON",
):
    """Fetch DAM price data from ERCOT and store in database.

    Args:
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        settlement_point: ERCOT settlement point (e.g., 'HB_HOUSTON')
    """
    logger.info(
        f"Fetching DAM data for {settlement_point} from {from_date} to {to_date}"
    )

    params = {
        "deliveryDateFrom": from_date,
        "deliveryDateTo": to_date,
        "settlementPoint": settlement_point,
        "page": 1,
    }

    req = ERCOTRequest(endpoint="np4-190-cd/dam_stlmnt_pnt_prices", params=params)
    raw_data = await req.fetch_ercot_data()
    logger.info(f"Fetched {len(raw_data)} rows from ERCOT API")

    processed_data = process_np_190_data(raw_data)
    logger.info(f"Processed data: {len(processed_data)} rows")

    location_df = pl.DataFrame(
        {
            "iso": ["ERCOT"] * len(processed_data),
            "location_type": ["settlement_point"] * len(processed_data),
            "location": processed_data["settlementPoint"].to_list(),
            "market": ["DA"] * len(processed_data),
            "resolution": ["hourly"] * len(processed_data),
        }
    ).unique()

    await upsert_price_locations(location_df)
    logger.info(f"Upserted {len(location_df)} locations")

    location_ids = []
    for loc in processed_data["settlementPoint"].unique().to_list():
        location_ids.append(await get_location_id("ERCOT", loc, "DA"))

    location_id_map = dict(
        zip(processed_data["settlementPoint"].unique().to_list(), location_ids)
    )

    processed_data = processed_data.with_columns(
        pl.col("settlementPoint").map_dict(location_id_map).alias("location_id")
    ).drop("settlementPoint")

    await upsert_price_data(processed_data)
    logger.info("DAM data fetch and store complete")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch ERCOT DAM data and store in database"
    )
    parser.add_argument("--from-date", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--to-date", required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument(
        "--settlement-point",
        default="HB_HOUSTON",
        help="Settlement point (default: HB_HOUSTON)",
    )

    args = parser.parse_args()

    asyncio.run(
        fetch_and_store_dam(
            from_date=args.from_date,
            to_date=args.to_date,
            settlement_point=args.settlement_point,
        )
    )


if __name__ == "__main__":
    main()

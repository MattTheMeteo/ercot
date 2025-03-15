from api_access import ERCOTRequest
import asyncio
params = {
            "deliveryDateFrom": "2024-07-01",
            "deliveryDateTo": "2025-03-01",
            "settlementPoint": "HB_HOUSTON",
            "page": 1,
        }
def main(params):
    req = ERCOTRequest(endpoint="np4-190-cd/dam_stlmnt_pnt_prices", params=params)
    out = asyncio.run(req.fetch_ercot_data())
    out.write_csv(file="/home/mlivingston/gs_data/HB_HOUSTON_ERCOT.csv")
    return out



if __name__ == "__main__":
    main()
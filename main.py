import os, requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

CTT_BASE   = "https://enviosecommerceapi.ctt.pt/v3"
CLIENT_ID  = os.getenv("CTT_3DF9E0E9-3FFC-38FE-ADD1-55012AAD4C37")
CLIENT_SEC = os.getenv("9F8AF421-DA10-3399-BCB0-53944941AFCE")

app = FastAPI()

@app.get("/pickup")
def get_pickup_points(postal_code: str):
    if not postal_code:
        raise HTTPException(400, "postal_code missing")

    headers = {
        "X-IBM-Client-Id":     CLIENT_ID,
        "X-IBM-Client-Secret": CLIENT_SEC,
    }

    try:
        r = requests.get(
            f"{CTT_BASE}/pickup-points",
            params={"postal_code": postal_code},
            headers=headers,
            timeout=6,
        )
        r.raise_for_status()
        data = r.json()
        return JSONResponse({"pickup_points": data.get("pickup_points", [])})
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code,
                            detail=e.response.text)
    except Exception as e:
        raise HTTPException(500, str(e))

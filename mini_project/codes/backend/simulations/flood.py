from fastapi import APIRouter

router = APIRouter()

@router.post("/flood")
def flood_predict(data: dict):
    lat = data.get("lat")
    lon = data.get("lon")

    # Simple demo logic (stable)
    elevation = 440 + (lat % 1) * 10
    rainfall = 1

    flood_risk = 1  # 1 = high (demo)

    return {
        "lat": lat,
        "lon": lon,
        "elevation": round(elevation, 2),
        "rainfall": rainfall,
        "flood_risk": flood_risk
    }

from fastapi import APIRouter
import numpy as np

router = APIRouter()

@router.post("/heat")
def heat_predict(data: dict):
    vegetation = data.get("vegetation", [])
    builtup = data.get("builtup", [])

    # Make sure arrays are same length
    size = min(len(vegetation), len(builtup))
    vegetation = vegetation[:size]
    builtup = builtup[:size]

    risk = []

    for v, b in zip(vegetation, builtup):
        # simple rule-based model
        if b > 0.6 and v < 0.3:
            risk.append(1)   # high heat risk
        else:
            risk.append(0)   # low heat risk

    return {
        "risk_layer": risk,
        "summary": "Heat risk based on vegetation + built-up ratio"
    }

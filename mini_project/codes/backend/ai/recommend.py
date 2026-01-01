import os
from fastapi import APIRouter
from groq import Groq

router = APIRouter()

GROQ_KEY = os.getenv("GROQ_API_KEY")

if GROQ_KEY:
    print("✅ GROQ_API_KEY loaded")
    client = Groq(api_key=GROQ_KEY)
else:
    print("❌ GROQ_API_KEY missing")
    client = None


@router.post("/recommend")
def recommend(data: dict):

    flood = data.get("flood", [])
    heat = data.get("heat", [])

    if client is None:
        return {
            "recommendations": "Groq API key not set."
        }

    prompt = f"""
You are an expert urban resilience planner.

Flood risk values: {flood}
Heat risk values: {heat}

Give short, clear, actionable recommendations for:
- Flood mitigation
- Heat mitigation
- Infrastructure resilience
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=400
        )

        return {
            "recommendations": response.choices[0].message.content
        }

    except Exception as e:
        print("❌ GROQ ERROR:", e)
        return {
            "recommendations": f"GROQ ERROR: {str(e)}"
        }

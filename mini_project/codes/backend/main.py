from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from simulations.flood import router as flood_router
from simulations.heat import router as heat_router
from ai.recommend import router as recommend_router

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(flood_router)
app.include_router(heat_router)
app.include_router(recommend_router)

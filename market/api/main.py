from fastapi import FastAPI
from market.api.endpoints import router

app = FastAPI()
app.include_router(router, tags=['MEGA MARKET API'])

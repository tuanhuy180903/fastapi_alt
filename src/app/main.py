from fastapi import FastAPI
app = FastAPI()

from app.database import db
from app.api import ping

db.init()
app.include_router(ping.router)

""" @app.get("/pong")
async def pong():
    return {"dd":"aa"} """

@app.on_event("startup")
async def startup():
    await db.create_all()

@app.on_event("shutdown")
async def shutdown():
    await db.close()

from app.api.views import *
apis = [api_fleets, api_fleet, api_vehicles, api_vehicle, api_drivers, api_driver, 
api_routes, api_route, api_routedetails, api_routedetail]

for api in apis:
    app.include_router(api)
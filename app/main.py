from fastapi import FastAPI
from app.controllers import scrape_routes

app = FastAPI()


@app.get("/")
async def root():
    return {'message':'Welcome to Resto Scrape API'}

app.include_router(scrape_routes.router)



    








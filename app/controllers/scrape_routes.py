from fastapi import APIRouter, BackgroundTasks
from app.models.schema import InputQuery
from app.services.services import scrape_resto

router = APIRouter(
    prefix='/data-scrape',
    tags=['scrape']
)

@router.post("/scrape_resto")
async def scrape_resto_data(input_query: InputQuery, backgroud_task: BackgroundTasks):
    backgroud_task.add_task(scrape_resto, input_query)
    return {'message':'Please Wait, We stil process your Scrape Request'}


        



import uvicorn
from fastapi import FastAPI, Query
from typing import List
from main import parse_b2b_center_selenium
from core import BASE_URL
from pydantic import BaseModel


class Tender(BaseModel):
    number: str
    link: str
    customer: str
    products: str
    deadline: str
    publish_date: str


app = FastAPI(title="FastAPI App V1", version="1.0.0")


@app.get("/tenders", response_model=List[Tender])
def get_tenders(max_results: int = Query(10, ge=1, le=100)):
    raw_tenders = parse_b2b_center_selenium(BASE_URL, max_results)
    return raw_tenders


if __name__ == "__main__":
    uvicorn.run("main_fastapi_v1:app", reload=True)

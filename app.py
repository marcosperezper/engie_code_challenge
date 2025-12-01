from typing import List

from fastapi import FastAPI
from schemas import ProductionRequest, ProductionResponse
from logic import compute_production_request

app = FastAPI(title="Production Request API")

@app.post("/productionplan", response_model=List[ProductionResponse])
async def produce_plan(request: ProductionRequest):
    try:
        result= compute_production_request(request)
        return result
    except Exception as e:
        return {"error": str(e)}
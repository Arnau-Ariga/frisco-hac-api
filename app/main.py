# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.hac_scraper import get_grades

app = FastAPI()

class HACRequest(BaseModel):
    username: str
    password: str
    district: str = "friscoisd"

@app.post("/grades")
async def grades(request: HACRequest):
    try:
        return get_grades(request.username, request.password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

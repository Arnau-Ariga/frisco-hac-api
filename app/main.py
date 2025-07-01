from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.hac_scraper import HACClient

app = FastAPI()

# ✅ Allow all origins (for dev) — replace with frontend URL in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["http://localhost:3000"] to restrict in dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/grades/transcript")
async def transcript_grades(req: LoginRequest):
    try:
        client = HACClient(req.username, req.password)
        grades = client.get_transcript_grades()
        return {"grades": grades}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/grades/testscores")
async def test_scores(req: LoginRequest):
    try:
        client = HACClient(req.username, req.password)
        scores = client.get_test_scores()
        return {"test_scores": scores}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/demographics")
async def demographics(req: LoginRequest):
    try:
        client = HACClient(req.username, req.password)
        data = client.get_demographics()
        return {"demographics": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/classes/classwork")
async def classwork(req: LoginRequest):
    try:
        client = HACClient(req.username, req.password)
        cw = client.get_classwork()
        return {"classwork": cw}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/home/schoollinks")
async def school_links(req: LoginRequest):
    try:
        client = HACClient(req.username, req.password)
        links = client.get_school_links()
        return {"school_links": links}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# backend/main.py
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from arq import ArqRedis
import asyncio

# --- NEW IMPORTS ---
from arq.worker import create_worker
from worker import WorkerSettings, get_redis_pool # Import your settings and pool

# --- END NEW IMPORTS ---

app = FastAPI()

# --- CORS Middleware ---
origins = [
    "http://localhost:3000",
    "https://ai-insights-app-lovat.vercel.app" # Add your Vercel URL
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models (unchanged) ---
class TranscriptRequest(BaseModel):
    transcript_text: str
    company_name: str
    attendees: List[str]
    date: str

class LinkedInRequest(BaseModel):
    linkedin_bio: str
    pitch_deck: str

# --- Redis Pool & Worker State ---
app.state.redis = None
app.state.worker = None
app.state.worker_task = None

@app.on_event("startup")
async def startup():
    # Start Redis pool
    app.state.redis = await get_redis_pool()
    
    # --- NEW: Start the worker in the background ---
    print("Starting ARQ worker in background...")
    worker = create_worker(WorkerSettings)
    app.state.worker_task = asyncio.create_task(worker.main())
    app.state.worker = worker
    print("ARQ worker started.")
    # --- END NEW ---

@app.on_event("shutdown")
async def shutdown():
    # Stop Redis pool
    await app.state.redis.close()
    
    # --- NEW: Stop the worker ---
    if app.state.worker:
        print("Stopping ARQ worker...")
        await app.state.worker.close()
        await app.state.worker_task
        print("ARQ worker stopped.")
    # --- END NEW ---

async def get_redis() -> ArqRedis:
    return app.state.redis

# --- Endpoints (unchanged) ---

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/insights/transcript")
async def create_transcript_insight(request: TranscriptRequest, redis: ArqRedis = Depends(get_redis)):
    metadata = {
        "company_name": request.company_name,
        "attendees": request.attendees,
        "date": request.date
    }
    insight_id = save_pending_insight(
        type="transcript",
        metadata=metadata,
        input_primary=request.transcript_text
    )
    await redis.enqueue_job(
        'run_transcript_insight',
        insight_id,
        request.transcript_text
    )
    return {"status": "processing", "id": insight_id}

@app.post("/insights/linkedin")
async def create_linkedin_insight(request: LinkedInRequest, redis: ArqRedis = Depends(get_redis)):
    metadata = { "source": "linkedin_bio" }
    insight_id = save_pending_insight(
        type="linkedin",
        metadata=metadata,
        input_primary=request.linkedin_bio
    )
    await redis.enqueue_job(
        'run_linkedin_icebreaker',
        insight_id,
        request.linkedin_bio,
        request.pitch_deck
    )
    return {"status": "processing", "id": insight_id}

# --- DB Service functions need to be imported ---
# (We put them here just to be safe, but they should be in db_service.py)
from db_service import save_pending_insight, get_all_insights

@app.get("/insights")
def read_all_insights():
    return get_all_insights()
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware # Import this

# Import your service functions
from ai_service import generate_transcript_insight, generate_linkedin_icebreaker
from db_service import save_insight, get_all_insights

app = FastAPI()

# --- THIS IS CRITICAL for your frontend ---
# Allow your Next.js app (running on localhost:3000) to talk to this API
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------------------------

# Pydantic models (data shapes)
class TranscriptRequest(BaseModel):
    transcript_text: str
    company_name: str
    attendees: List[str]
    date: str

class LinkedInRequest(BaseModel):
    linkedin_bio: str
    pitch_deck: str

# API Endpoints
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/insights/transcript")
def create_transcript_insight(request: TranscriptRequest):
    # 1. Get AI analysis
    analysis = generate_transcript_insight(request.transcript_text)

    # 2. Format metadata
    metadata = {
        "company_name": request.company_name,
        "attendees": request.attendees,
        "date": request.date
    }

    # 3. Save to database
    saved_data = save_insight(
        type="transcript",
        metadata=metadata,
        input_primary=request.transcript_text,
        output=analysis
    )

    return saved_data

@app.post("/insights/linkedin")
def create_linkedin_insight(request: LinkedInRequest):
    # 1. Get AI analysis
    analysis = generate_linkedin_icebreaker(
        bio=request.linkedin_bio,
        pitch_deck=request.pitch_deck
    )
    
    # 2. Format metadata (it's simpler for this one)
    metadata = { "source": "linkedin_bio" }
    
    # 3. Save to database (we reuse the same function!)
    saved_data = save_insight(
        type="linkedin",
        metadata=metadata,
        input_primary=request.linkedin_bio, # Store the bio
        output=analysis
    )
    
    return saved_data

@app.get("/insights")
def read_all_insights():
    return get_all_insights()
# backend/worker.py
import os
from dotenv import load_dotenv
from arq import create_pool, ArqRedis
from arq.connections import RedisSettings

# Import your existing AI and DB functions
# We will create 'update_insight_analysis' in the next step
from ai_service import generate_transcript_insight, generate_linkedin_icebreaker
from db_service import update_insight_analysis 

load_dotenv()

# --- Arq Task Definitions ---

async def run_transcript_insight(ctx, insight_id, transcript_text):
    """
    This is the background job for transcripts.
    'ctx' is a required argument for arq, it contains job context.
    """
    print(f"Processing insight {insight_id}...")
    
    # 1. Run the expensive AI call
    analysis = generate_transcript_insight(transcript_text)
    
    # 2. Update the database row with the final result
    update_insight_analysis(insight_id, analysis)
    
    print(f"Completed insight {insight_id}")

async def run_linkedin_icebreaker(ctx, insight_id, bio, deck):
    """
    This is the background job for LinkedIn.
    """
    print(f"Processing insight {insight_id}...")
    
    # 1. Run the expensive AI call
    analysis = generate_linkedin_icebreaker(bio, deck)
    
    # 2. Update the database row with the final result
    update_insight_analysis(insight_id, analysis)
    
    print(f"Completed insight {insight_id}")

# --- Arq Worker Settings ---

# This tells Arq how to connect to your Upstash Redis
def get_redis_settings():
    return RedisSettings(
        host=os.getenv("UPSTASH_REDIS_HOST"),    # The "Endpoint" you copied
        password=os.getenv("UPSTASH_REDIS_PASSWORD"), # The "Token" you copied
        port=6379,  # Default Redis port
        ssl=True    # Upstash requires SSL
    )

# This defines the functions that the worker can run
class WorkerSettings:
    functions = [run_transcript_insight, run_linkedin_icebreaker]
    redis_settings = get_redis_settings()

# This is a helper function for main.py to get a connection
async def get_redis_pool() -> ArqRedis:
    return await create_pool(WorkerSettings.redis_settings)
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
# Initialize the Groq client
# It automatically reads the GROQ_API_KEY from your .env file
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Specify the model you want to use
GROQ_MODEL = "llama-3.1-8b-instant"


# --- FUNCTION 1 (This is what's missing) ---
def generate_transcript_insight(transcript: str) -> str:
    # Your sample prompt
    prompt = f"review this transcript and share what I did well and why, what I could do even better and recommendations of things I can test differently next time.\n\nTranscript: {transcript}"
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=GROQ_MODEL,
    )
    return chat_completion.choices[0].message.content


# --- FUNCTION 2 (You added this one) ---
def generate_linkedin_icebreaker(bio: str, pitch_deck: str) -> str:
    # This is your powerful prompt
    prompt = f"""
    Here is a LinkedIn -about section:
    ---
    {bio}
    ---

    Here is my company's pitch deck summary:
    ---
    {pitch_deck}
    ---

    Based on this information, please provide the following:
    1.  Buying signals for my company based on their bio (list them, why they matter, and the source/trigger).
    2.  Smart discovery questions to ask in your next call, both at the company and role level.
    3.  What is this person's preferred style of buying, and how did you infer that?
    4.  A short summary of your analysis.
    5.  3 reflection questions for me to prepare better for the meet.
    6.  Top 5 things they would likely want from our deck.
    7.  What parts of the deck may not be clear, relevant, or valuable to them and why + what to do instead.
    """
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a world-class sales development and market research assistant."
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=GROQ_MODEL,
    )
    return chat_completion.choices[0].message.content
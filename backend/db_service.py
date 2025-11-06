# backend/db_service.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def save_pending_insight(type: str, metadata: dict, input_primary: str):
    """
    Saves the initial job with a 'Processing...' status.
    Returns the ID of the new row.
    """
    data = {
        "type": type,
        "metadata": metadata,
        "input_primary": input_primary,
        "output_analysis": "Processing..." # <-- New default status
    }
    try:
        # 'insights' is the table name
        response = supabase.table('insights').insert(data).execute()
        return response.data[0]['id'] # <-- Return the new ID
    except Exception as e:
        print(f"Error saving pending insight: {e}")
        return None

def update_insight_analysis(insight_id: int, analysis: str):
    """
    Updates the insight row with the final AI-generated text.
    """
    try:
        supabase.table('insights').update({
            'output_analysis': analysis
        }).eq('id', insight_id).execute()
    except Exception as e:
        print(f"Error updating insight {insight_id}: {e}")

def get_all_insights():
    """
    This function is unchanged.
    """
    try:
        response = supabase.table('insights').select("*").order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Error fetching from Supabase: {e}")
        return []
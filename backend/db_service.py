import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def save_insight(type: str, metadata: dict, input_primary: str, output: str):
    data = {
        "type": type,
        "metadata": metadata,
        "input_primary": input_primary,
        "output_analysis": output
    }
    try:
        # 'insights' is the table name you created
        response = supabase.table('insights').insert(data).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error saving to Supabase: {e}")
        return None

def get_all_insights():
    try:
        response = supabase.table('insights').select("*").order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Error fetching from Supabase: {e}")
        return []
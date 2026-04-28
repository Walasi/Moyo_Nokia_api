import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def log_claim(phone, location, reason, status, tx_id=None):
    supabase.table("claims").insert({
        "phone_number": phone,
        "location": location,
        "reason": reason,
        "status": status,
        "tx_id": tx_id
    }).execute()
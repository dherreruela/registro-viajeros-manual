from supabase import create_client
import os
from dotenv import load_dotenv
from pathlib import Path

backend_dir = Path(__file__).parent.parent
env_path = backend_dir / ".env"
load_dotenv(dotenv_path=env_path)

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL y SUPABASE_KEY no están configuradas en .env")

supabase = create_client(supabase_url, supabase_key)

def get_supabase():
    return supabase

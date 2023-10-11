import os
from supabase import create_client, Client

URL: str = os.environ.get("SUPABASE_URL")
KEY: str = os.environ.get("SUPABASE_KEY")


def get_supabase_client() -> Client:
    return create_client(URL, KEY)

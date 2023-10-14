from supabase import Client


def get_managers_with_name(supabase: Client, name: str):
    data, _ = supabase.table("managers").select("*").eq("name", name).execute()
    return data

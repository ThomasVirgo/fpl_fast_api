from typing import Dict, Optional
from supabase import Client


def get_managers_with_name(supabase: Client, name: str):
    data, _ = supabase.table("managers").select("*").eq("name", name).execute()
    return data


def get_latest_h2h_stats_for_league(supabase: Client, league_id: int) -> Optional[Dict]:
    latest = (
        supabase.table("h2h")
        .select("stats", "created_at")
        .eq("league_id", league_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if len(latest.data) == 0:
        return None
    return latest.data[0]


def get_latest_manager_stats(supabase: Client, manager_id: int) -> Optional[Dict]:
    latest = (
        supabase.table("manager_stats")
        .select("stats")
        .eq("league_id", manager_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if len(latest.data) == 0:
        return None
    return latest

from dataclasses import asdict

from fastapi import FastAPI, Request, Form

from fastapi.templating import Jinja2Templates

from fpl.data_loading import create_fpl_data, create_h2h_data, get_overview
from fpl.logic import FplWrapped
from fpl.utils import H2HRow, extract_h2h_rows, requires_reload
from fpl.db.client import get_supabase_client
from fpl.db.query import get_latest_h2h_stats_for_league, get_managers_with_name

app = FastAPI()


templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.get("/manager/{manager_id}")
def manager(request: Request, manager_id: int):
    fpl_data = create_fpl_data(manager_id)
    fpl_wrapped = FplWrapped(fpl_data)
    rows = fpl_wrapped.captaincy()
    correct_captaincy = 0
    incorrect_captaincy = 0
    points_lost = 0
    for row in rows:
        if row.captain_name == row.highest_scorer_name:
            correct_captaincy += 1
        else:
            incorrect_captaincy += 1
            points_lost += row.highest_scorer_points_if_captain - row.captain_points
    gameweek_to_rank = fpl_wrapped.fpl_data.manager_history.gameweek_to_overall_rank
    gameweeks = []
    ranks = []
    for gw, rank in gameweek_to_rank.items():
        gameweeks.append(gw)
        ranks.append(rank)
    return templates.TemplateResponse(
        "fpl_wrapped.html",
        context={
            "request": request,
            "rows": rows,
            "points_lost": points_lost,
            "correct_captaincy": correct_captaincy,
            "incorrect_captaincy": incorrect_captaincy,
            "gameweeks": gameweeks,
            "ranks": ranks,
        },
    )


@app.post("/")
def search(request: Request, name: str = Form(...)):
    supabase = get_supabase_client()
    managers = get_managers_with_name(supabase, name)[1]
    return templates.TemplateResponse(
        "index.html", context={"request": request, "managers": managers}
    )


@app.get("/h2h/{league_id}")
def h2h(request: Request, league_id: int):
    supabase = get_supabase_client()
    latest_stats_for_league = get_latest_h2h_stats_for_league(supabase, league_id)
    needs_reload = True

    if latest_stats_for_league:
        created_at = latest_stats_for_league["created_at"]
        overview = get_overview()
        needs_reload = requires_reload(overview, created_at)

    if needs_reload:
        h2h_data = create_h2h_data(league_id)
        rows = extract_h2h_rows(h2h_data)
        supabase.table("h2h").insert(
            {"league_id": league_id, "stats": [asdict(x) for x in rows]}
        ).execute()
    else:
        rows = [H2HRow(**row) for row in latest_stats_for_league["stats"]]

    return templates.TemplateResponse(
        "h2h.html", context={"request": request, "rows": rows}
    )

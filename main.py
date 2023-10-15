from dataclasses import asdict

from fastapi import FastAPI, Request, Form

from fastapi.templating import Jinja2Templates

from fpl.data_loading import create_fpl_data, create_h2h_data
from fpl.logic import FplWrapped
from fpl.utils import H2HRow, extract_h2h_rows
from fpl.db.client import get_supabase_client
from fpl.db.query import get_managers_with_name

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
    return templates.TemplateResponse(
        "fpl_wrapped.html",
        context={
            "request": request,
            "rows": rows,
            "points_lost": points_lost,
            "correct_captaincy": correct_captaincy,
            "incorrect_captaincy": incorrect_captaincy,
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
    latest_stats_for_league = (
        supabase.table("h2h")
        .select("stats")
        .eq("league_id", league_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    try:
        rows = [H2HRow(**row) for row in latest_stats_for_league.data[0]["stats"]]
    except:
        h2h_data = create_h2h_data(league_id)
        rows = extract_h2h_rows(h2h_data)

    # data, count = (
    #     supabase.table("h2h")
    #     .insert({"league_id": league_id, "stats": [asdict(x) for x in rows]})
    #     .execute()
    # )
    return templates.TemplateResponse(
        "h2h.html", context={"request": request, "rows": rows}
    )

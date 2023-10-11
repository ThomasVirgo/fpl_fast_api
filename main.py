from dataclasses import asdict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from fpl.data_loading import create_fpl_data, create_h2h_data
from fpl.logic import FplWrapped
from fpl.utils import H2HRow, extract_h2h_rows
from fpl.db.client import get_supabase_client

app = FastAPI()

origins = ["*"]

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "welcome to fpl wrapped"}


@app.get("/manager/{manager_id}")
def manager(manager_id: int):
    fpl_data = create_fpl_data(manager_id)
    fpl_wrapped = FplWrapped(fpl_data)
    return fpl_wrapped.captaincy()


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

from fastapi import FastAPI

from fpl.client import FPLClient, get_overview_and_create_endpoint_to_schema

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "welcome to fpl wrapped"}


@app.get("/fpl/{manager_id}")
def fpl(manager_id: int):
    overview, endpoint_to_schema = get_overview_and_create_endpoint_to_schema(
        manager_id
    )
    fpl_client = FPLClient(endpoint_to_schema)
    fpl_data = fpl_client.retrieve_all_data()
    fpl_data["overview"] = overview
    return fpl_data

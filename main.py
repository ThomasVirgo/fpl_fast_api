from fastapi import FastAPI

from fpl.client import FPLClient

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "welcome to fpl wrapped"}


@app.get("/fpl/{manager_id}")
def fpl(manager_id: int):
    fpl_client = FPLClient(manager_id)
    return fpl_client.retrieve_data_from_endpoints()

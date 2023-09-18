from typing import Optional

from fastapi import FastAPI

from fpl.client import FPLClient

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/items/{manager_id}")
def read_item(manager_id: int):
    fpl_client = FPLClient(manager_id)
    return fpl_client.retrieve_data_from_endpoints()

from fastapi import FastAPI

from fpl.client import create_fpl_data

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "welcome to fpl wrapped"}


@app.get("/fpl/{manager_id}")
def fpl(manager_id: int):
    return create_fpl_data(manager_id)

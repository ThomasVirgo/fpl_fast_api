from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fpl.data_loading import create_fpl_data
from fpl.logic import FplWrapped

app = FastAPI()

origins = ["*"]

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


@app.get("/fpl/{manager_id}")
def fpl(manager_id: int):
    fpl_data = create_fpl_data(manager_id)
    fpl_wrapped = FplWrapped(fpl_data)
    return fpl_wrapped.captaincy()

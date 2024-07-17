print("loading...")
print("load db...")
import json

db = {}

with open("./db.json", "r") as file:
    try:
        db = json.loads(file.read())
    except json.decoder.JSONDecodeError as err:
        print(f"Error on line 9: {err}")
        db = {}
    
print("load FastAPI")

from typing import Union

from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

print("end")

app = FastAPI()

origins = [
    "https://localhost",  # 허용할 도메인
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return db

@app.post("/add")
def add(gold: int, country: str):
    try:
        db[country] += gold
    except KeyError:
        db[country] = gold
    return db

@app.post("/subtract")
def subtract(gold: int, country: str):
    try:
        if gold <= db[country]:
            db[country] -= gold
        else:
            return {"error": "795"} # 돈 없어요;;
    except KeyError:
        return {"error": "795"} # 돈 없어요;;
    return db

@app.on_event("shutdown")
def shutdown_event():
    with open("db.json", mode="w") as dbfile:
        dbfile.write(json.dumps(db))
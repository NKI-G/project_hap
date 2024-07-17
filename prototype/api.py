print("loading...")
print("load db...")
import json
from fastapi import FastAPI, HTTPException, Request, status
from typing import Dict
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

# Initialize database and debug variables
db: Dict[str, int] = {}
debug: bool = False

# Load database from file
try:
    with open("./db.json", "r") as file:
        db = json.load(file)
except (FileNotFoundError, json.JSONDecodeError) as err:
    print(f"Error loading db.json: {err}")
    db = {}

# Load settings from file
try:
    with open("./setting.json", "r") as file:
        settings = json.load(file)
        debug = settings.get("debug", False)
except (FileNotFoundError, json.JSONDecodeError) as err:
    print(f"Error loading setting.json: {err}")

print("load FastAPI")

app = FastAPI()

# Configure CORS
if debug:
    print("Debug mode enabled")
    origins = [
        "localhost",
        "localhost:8000",
        "127.0.0.1:8000",
        "127.0.0.1",
    ]
else:
    print("Production mode enabled")
    origins = [
        "http://at.at",
    ]

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("CORS origins set to:", origins)
print("end")
print(f"Debug: {debug}")

@app.middleware('http')
async def validate_ip(request: Request, call_next):
    # Get client IP
    client_ip = request.client.host
    
    # Check if IP is allowed
    if client_ip not in origins:
        print(origins)
        data = {
            'message': f'IP {client_ip} is not allowed to access this resource.'
        }
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=data)

    # Proceed if IP is allowed
    return await call_next(request)

@app.get("/")
def read_root():
    print("Returning database contents")
    return db

@app.post("/add")
def add_gold(gold: int, country: str):
    if country in db:
        db[country] += gold
    else:
        db[country] = gold
    return db

@app.post("/subtract")
def subtract_gold(gold: int, country: str):
    if country not in db or db[country] < gold:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    db[country] -= gold
    return db

@app.on_event("shutdown")
def shutdown_event():
    try:
        with open("db.json", "w") as dbfile:
            json.dump(db, dbfile)
    except IOError as err:
        print(f"Error saving db.json: {err}")
from fastapi import FastAPI
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from database import create_db_and_tables, engine
from fastapi.middleware.cors import CORSMiddleware
import hashlib

from models import User, UserLogin, Drink

def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/User")
async def root():
    return {"message": "ANG INIT"}


@app.get("/User/{id}")
async def read_user(id: int):
    with Session(engine) as session:
        user = session.get(User, id)
        return {"message": user}


@app.post("/register")
async def register(user: User):
    with Session(engine) as session:
        user.username = hash_text(user.username)
        user.password = hash_text(user.password)
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"message": user}


@app.post("/login")
async def login(data: UserLogin):
    with Session(engine) as session:
        user = session.exec(
            select(User).where(
                User.username == hash_text(data.username),
                User.password == hash_text(data.password)
            )
        ).first()
        return {"message": user}


@app.get("/drinks")
async def get_drinks():
    with Session(engine) as session:
        drinks = session.exec(select(Drink)).all()
        return {"message": drinks}


@app.post("/drinks")
async def add_drink(drink: Drink):
    with Session(engine) as session:
        session.add(drink)
        session.commit()
        session.refresh(drink)
        return {"message": drink}
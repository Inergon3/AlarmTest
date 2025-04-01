from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from fastapi_users.schemas import BaseUser
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth import auth_backend
from app.auth.database import User
from app.auth.manager import get_user_manager
from app.auth.schemas import UserRead, UserCreate
from app.crud import (
    get_all_alarms, get_alarm_by_id, add_alarm, remove_alarm, remove_all_alarms, edit_alarm_by_id
)
from app.models import SessionLocal

app = FastAPI()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],

)

current_user = fastapi_users.current_user()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/alarm/{alarm_id}")
def get_alarm(alarm_id: int, db: AsyncSession = Depends(get_db)):
    return get_alarm_by_id(db, alarm_id)


@app.post("/alarm/add/{alarm_id}")
def add_new_alarm(alarm_id: int, time: str, db: AsyncSession = Depends(get_db)):
    return add_alarm(db, time, alarm_id)
# def add_new_alarm(time: str, db: Session = Depends(get_db)):
#     return add_alarm(db, time)


@app.get("/alarm")
def get_all_alarms_route(db: AsyncSession = Depends(get_db)):
    return get_all_alarms(db)


@app.delete("/alarm/remove/{alarm_id}")
def remove_alarm_by_id(alarm_id: int, db: AsyncSession = Depends(get_db)):
    return remove_alarm(db, alarm_id)


@app.delete("/alarm/all_remove")
def remove_all_alarms_route(db: AsyncSession = Depends(get_db)):
    return remove_all_alarms(db)


@app.put("/alarm/edit/{alarm_id}")
def edit_alarm(alarm_id: int, time: str, db: AsyncSession = Depends(get_db)):
    return edit_alarm_by_id(db, alarm_id, time)

@app.get("/")
def hello():
    return "Hello"
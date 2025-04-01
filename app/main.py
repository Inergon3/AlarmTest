from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr, BaseModel
from app.auth.auth import auth_backend
from app.auth.database import User
from app.auth.manager import get_user_manager
from app.auth.schemas import UserRead, UserCreate
from app.crud import (
    add_alarm, get_all_alarms_by_user, remove_alarm_by_user, edit_alarm_by_user_by_id
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


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


# @app.get("/alarm/{alarm_id}")
# async def get_alarm(alarm_id: int, db: AsyncSession = Depends(get_db)):
#     return await get_alarm_by_id(db, alarm_id)


@app.post("/alarm/add")
async def add_new_alarm(time: str, db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    return await add_alarm(db, time, user)


@app.get("/alarm")
async def get_all_alarms_by_users(db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    return await get_all_alarms_by_user(db, user)


@app.delete("/alarm/remove")
async def remove_alarm_by_users(db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    return await remove_alarm_by_user(db, user)


# @app.delete("/alarm/all_remove")
# async def remove_all_alarms_route(db: AsyncSession = Depends(get_db)):
#     return await remove_all_alarms(db)


@app.put("/alarm/edit/{alarm_id}")
async def edit_alarm(alarm_id: int, time: str, db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    return await edit_alarm_by_user_by_id(db, alarm_id, time, user)


@app.get("/")
async def hello():
    return "Hello"

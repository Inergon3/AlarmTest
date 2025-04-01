from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AlarmsModel


async def get_all_alarms_by_user(db: AsyncSession, user):
    result = await find_alarm_by_user_id(db, user)
    alarms = result.scalars().all()
    return alarms


# def get_alarm_by_id(db: AsyncSession, alarm_id: int):
#     alarm = find_alarm_by_id(db, alarm_id)
#     if not alarm:
#         raise HTTPException(status_code=404, detail="Будильник не найден")
#     return alarm


async def add_alarm(db: AsyncSession, time: str, user):
    if user:
        new_alarm = AlarmsModel(alarm=time, user_id=user.id)
        db.add(new_alarm)
        await db.commit()
        return new_alarm
    raise HTTPException(status_code=401, detail="Вы не авторизованы")


async def remove_alarm_by_user(db: AsyncSession, user):
    if user:
        result = await find_alarm_by_user_id(db, user)
        alarms = result.scalars().all()
        for alarm in alarms:
            await db.delete(alarm)
        await db.commit()
        return {"message": "Будильники удалены"}
    raise HTTPException(status_code=401, detail="Вы не авторизованы")


# def remove_all_alarms(db: AsyncSession, user):
#     db.query(AlarmsModel).delete()
#     db.commit()
#     return {"message": "Все будильники удалены"}


async def edit_alarm_by_user_by_id(db: AsyncSession, alarm_id: int, time: str, user):
    if user:
        result = await find_alarm_by_user_id(db, user, alarm_id)
        alarms = result.scalars().first()
        if alarms is not None:
            alarms.alarm = time
            await db.commit()
            return {"message": "Будильник изменен>"}
        raise HTTPException(status_code=404, detail="Будильник не найден")
    raise HTTPException(status_code=401, detail="Вы не авторизованы")


async def find_alarm_by_user_id(db: AsyncSession, user, alarm_id=None):
    if alarm_id is None:
        result = await db.execute(select(AlarmsModel).filter(AlarmsModel.user_id == user.id))
        return result
    result = await db.execute(select(AlarmsModel).filter(AlarmsModel.user_id == user.id, AlarmsModel.id == alarm_id))
    return result

from fastapi import HTTPException
from fastapi_users.schemas import BaseUser
from sqlalchemy.orm import Session

from app.models import AlarmsModel


def get_all_alarms(db: Session):
    alarms = db.query(AlarmsModel).all()
    return alarms


def get_alarm_by_id(db: Session, alarm_id: int):
    alarm = find_alarm_by_id(db, alarm_id)
    if not alarm:
        raise HTTPException(status_code=404, detail="Будильник не найден")
    return alarm


def add_alarm(db: Session, time: str, alarm_id: int):
    new_alarm = AlarmsModel(id = alarm_id, alarm=time)
    db.add(new_alarm)
    db.commit()
    return new_alarm


def remove_alarm(db: Session, alarm_id: int):
    alarm = find_alarm_by_id(db, alarm_id)
    if not alarm:
        raise HTTPException(status_code=404, detail="Будильник не найден")
    db.delete(alarm)
    db.commit()
    return {"message": "Будильник удален"}


def remove_all_alarms(db: Session):
    db.query(AlarmsModel).delete()
    db.commit()
    return {"message": "Все будильники удалены"}


def edit_alarm_by_id(db: Session, alarm_id: int, time: str):
    alarm = find_alarm_by_id(db, alarm_id)
    if alarm:
        alarm.alarm = time
        db.commit()
        return {"message": "Будильник изменен>"}
    raise HTTPException(status_code=404, detail="Будильник не найден")


def find_alarm_by_id(db: Session, alarm_id: int):
    alarm = db.query(AlarmsModel).filter(AlarmsModel.id == int(alarm_id)).first()
    return alarm

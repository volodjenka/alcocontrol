from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_telegram_id(db: Session, telegram_id: int):
    return db.query(models.User).filter(models.User.telegram_id == telegram_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_drinks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Drink).offset(skip).limit(limit).all()

def create_drink(db: Session, drink: schemas.DrinkCreate):
    db_drink = models.Drink(**drink.dict())
    db.add(db_drink)
    db.commit()
    db.refresh(db_drink)
    return db_drink

def get_sober_periods(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SoberPeriod).offset(skip).limit(limit).all()

def create_sober_period(db: Session, period: schemas.SoberPeriodCreate):
    db_period = models.SoberPeriod(**period.dict())
    db.add(db_period)
    db.commit()
    db.refresh(db_period)
    return db_period

def get_goals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Goal).offset(skip).limit(limit).all()

def create_goal(db: Session, goal: schemas.GoalCreate):
    db_goal = models.Goal(**goal.dict())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def get_user_drinks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Drink).filter(models.Drink.user_id == user_id).offset(skip).limit(limit).all()

def get_user_sober_periods(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.SoberPeriod).filter(models.SoberPeriod.user_id == user_id).offset(skip).limit(limit).all()

def get_user_goals(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Goal).filter(models.Goal.user_id == user_id).offset(skip).limit(limit).all()

def get_active_sober_period(db: Session, user_id: int):
    return db.query(models.SoberPeriod).filter(
        models.SoberPeriod.user_id == user_id,
        models.SoberPeriod.is_active == True
    ).first()

def end_sober_period(db: Session, period_id: int):
    period = db.query(models.SoberPeriod).filter(models.SoberPeriod.id == period_id).first()
    if period:
        period.is_active = False
        period.end_time = datetime.utcnow()
        db.commit()
        db.refresh(period)
    return period 
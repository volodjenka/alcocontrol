from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse

from . import models, schemas, crud
from .database import SessionLocal, engine
from .telegram_bot import setup_bot

# Загрузка переменных окружения
load_dotenv()

# Создание таблиц
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AlcoControl API")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Инициализация бота
bot = setup_bot()

# Обработчики ошибок
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error occurred: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unexpected error occurred: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

@app.get("/")
async def root():
    return {"message": "Welcome to AlcoControl API"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud.get_user_by_telegram_id(db, telegram_id=user.telegram_id)
        if db_user:
            raise HTTPException(status_code=400, detail="Telegram ID already registered")
        return crud.create_user(db=db, user=user)
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create user"
        )

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = crud.get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not read user"
        )

@app.post("/drinks/", response_model=schemas.Drink)
def create_drink(drink: schemas.DrinkCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_drink(db=db, drink=drink)
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating drink: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create drink"
        )

@app.get("/drinks/", response_model=List[schemas.Drink])
def read_drinks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        drinks = crud.get_drinks(db, skip=skip, limit=limit)
        return drinks
    except Exception as e:
        logger.error(f"Error reading drinks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not read drinks"
        )

@app.post("/sober-periods/", response_model=schemas.SoberPeriod)
def create_sober_period(period: schemas.SoberPeriodCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_sober_period(db=db, period=period)
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating sober period: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create sober period"
        )

@app.get("/sober-periods/", response_model=List[schemas.SoberPeriod])
def read_sober_periods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        periods = crud.get_sober_periods(db, skip=skip, limit=limit)
        return periods
    except Exception as e:
        logger.error(f"Error reading sober periods: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not read sober periods"
        )

@app.post("/goals/", response_model=schemas.Goal)
def create_goal(goal: schemas.GoalCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_goal(db=db, goal=goal)
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating goal: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create goal"
        )

@app.get("/goals/", response_model=List[schemas.Goal])
def read_goals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        goals = crud.get_goals(db, skip=skip, limit=limit)
        return goals
    except Exception as e:
        logger.error(f"Error reading goals: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not read goals"
        )

@app.get("/statistics/")
def get_statistics(user_id: int, db: Session = Depends(get_db)):
    try:
        # Получаем все напитки пользователя
        drinks = db.query(models.Drink).filter(models.Drink.user_id == user_id).all()
        
        # Считаем общее количество алкоголя
        total_alcohol = sum(drink.volume * drink.alcohol_content / 100 for drink in drinks)
        
        # Считаем количество дней с употреблением
        days_with_drinks = len(set(drink.created_at.date() for drink in drinks))
        
        # Получаем текущий период трезвости
        current_period = db.query(models.SoberPeriod).filter(
            models.SoberPeriod.user_id == user_id,
            models.SoberPeriod.end_date == None
        ).first()
        
        sober_days = 0
        if current_period:
            sober_days = (datetime.now() - current_period.start_date).days
        
        return {
            "total_alcohol": total_alcohol,
            "days_with_drinks": days_with_drinks,
            "sober_days": sober_days
        }
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not get statistics"
        ) 
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    settings: Optional[dict] = {}

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class DrinkBase(BaseModel):
    drink_type: str
    volume: float
    alcohol_content: float
    price: Optional[float] = None
    location: Optional[str] = None
    mood: Optional[str] = None
    comment: Optional[str] = None

class DrinkCreate(DrinkBase):
    user_id: int

class Drink(DrinkBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SoberPeriodBase(BaseModel):
    start_time: datetime
    end_time: Optional[datetime] = None
    is_active: bool = True

class SoberPeriodCreate(SoberPeriodBase):
    user_id: int

class SoberPeriod(SoberPeriodBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class GoalBase(BaseModel):
    type: str
    target_value: float
    period: str
    start_date: datetime
    end_date: Optional[datetime] = None
    is_active: bool = True

class GoalCreate(GoalBase):
    user_id: int

class Goal(GoalBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True 
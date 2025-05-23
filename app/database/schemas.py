from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime




class ClientBase(BaseModel):
    full_name: str
    phone: str
    email: str
    pass_num: Optional[str] = None
    born_date: str  # Дата в строковом формате "дд-мм-гггг"
    reg_date: Optional[str] = None  # Это может быть строкой с датой регистрации


class ClientUpdate(ClientBase):
    userId: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    pass_num: Optional[str] = None
    born_date: Optional[str] = None



# Объединяем модели запроса
class BookingCreateRequest(BaseModel):
    in_date: str
    name: str
    out_date: str
    phone: int
    room: int
    day_price: int



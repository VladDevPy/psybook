from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class SlotOut(BaseModel):
    slot_id: str
    start_local: datetime
    end_local: datetime
    available: bool

class BookingIn(BaseModel):
    slot_id: str = Field(min_length=1)
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr

class BookingOut(BaseModel):
    booking_id: str
    slot_id: str
    start_local: datetime
    end_local: datetime
    name: str
    email: EmailStr

class CancelIn(BaseModel):
    booking_id: str
    email: EmailStr
from pydantic import BaseModel
from datetime import date
from typing import Optional

# ==================== PROPERTIES ====================
class PropertyCreate(BaseModel):
    name: str
    google_calendar_id: str
    address: Optional[str] = None

class Property(PropertyCreate):
    id: int
    created_at: str

# ==================== RESERVATIONS ====================
class ReservationCreate(BaseModel):
    property_id: int
    reservation_code: str
    guest_name: str
    check_in: date
    check_out: date
    num_guests: int
    platform: Optional[str] = None  # 'airbnb' o 'booking'
    notes: Optional[str] = None

class ReservationUpdate(BaseModel):
    guest_name: Optional[str] = None
    check_in: Optional[date] = None
    check_out: Optional[date] = None
    num_guests: Optional[int] = None
    notes: Optional[str] = None
    processed: Optional[bool] = None

class Reservation(ReservationCreate):
    id: int
    processed: bool
    calendar_event_id: Optional[str] = None
    created_at: str
    updated_at: str

# ==================== GUESTS ====================
class GuestCreate(BaseModel):
    reservation_id: int
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    document_type: Optional[str] = None
    document_number: Optional[str] = None
    nationality: Optional[str] = None
    notes: Optional[str] = None

class Guest(GuestCreate):
    id: int
    created_at: str

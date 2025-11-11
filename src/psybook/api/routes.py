from datetime import date
from fastapi import APIRouter, HTTPException
from psybook.models.schemas import (
    SlotOut,
    BookingIn,
    BookingOut,
    CancelIn,
)
from psybook.services.booking_service import (
    list_slots_for_date,
    create_booking,
    cancel_booking,
)

router = APIRouter(tags=["booking"])


@router.get("/slots", response_model=list[SlotOut])
def get_slots(day: date) -> list[SlotOut]:
    return list_slots_for_date(day)


@router.post("/bookings", response_model=BookingOut, status_code=201)
def post_booking(payload: BookingIn) -> BookingOut:
    booking = create_booking(payload)
    if booking is None:
        raise HTTPException(status_code=409, detail="Slot is already booked")
    return booking


@router.post("/bookings/cancel", status_code=204)
def post_cancel(payload: CancelIn) -> None:
    ok = cancel_booking(payload.booking_id, payload.email)
    if not ok:
        raise HTTPException(
            status_code=404, detail="Booking not found or email mismatch"
        )

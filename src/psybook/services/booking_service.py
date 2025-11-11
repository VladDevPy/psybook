from __future__ import annotations
from datetime import date
from psybook.infra.memory_store import STORE, AMS
from psybook.models.schemas import SlotOut, BookingIn, BookingOut


def _to_slot_out(slot) -> SlotOut:
    start_local = slot.start_utc.astimezone(AMS)
    end_local = slot.end_utc.astimezone(AMS)
    return SlotOut(
        slot_id=slot.slot_id,
        start_local=start_local,
        end_local=end_local,
        available=True,
    )


def list_slots_for_date(day: date) -> list[SlotOut]:
    import asyncio

    slots = asyncio.run(STORE.list_slots_for_day(day))
    # отмечаем занятые
    booked_ids = {b.slot_id for b in STORE._bookings.values()}  # noqa: SLF001

    outs: list[SlotOut] = []
    for s in slots:
        out = _to_slot_out(s)
        out.available = s.slot_id not in booked_ids
        outs.append(out)

    outs.sort(key=lambda x: x.start_local)
    return outs


def create_booking(payload: BookingIn) -> BookingOut | None:
    import asyncio

    b = asyncio.run(STORE.create_booking(payload.slot_id, payload.name, payload.email))
    if b is None:
        return None

    slot = STORE._slots[b.slot_id]  # noqa: SLF001
    return BookingOut(
        booking_id=b.booking_id,
        slot_id=b.slot_id,
        start_local=slot.start_utc.astimezone(AMS),
        end_local=slot.end_utc.astimezone(AMS),
        name=b.name,
        email=b.email,
    )


def cancel_booking(booking_id: str, email: str) -> bool:
    import asyncio
    return asyncio.run(STORE.cancel_booking(booking_id, email))
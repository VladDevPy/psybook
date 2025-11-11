from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo
import uuid
import asyncio

AMS = ZoneInfo("Europe/Amsterdam")

@dataclass
class Slot:
    slot_id: str
    start_utc: datetime
    end_utc: datetime

@dataclass
class Booking:
    booking_id: str
    slot_id: str
    name: str
    email: str

class MemoryStore:
    """
    Простейшее in-memory хранилище (потокобезопасно под один процесс).
    """
    def __init__(self) -> None:
        self._slots: dict[str, Slot] = {}
        self._bookings: dict[str, Booking] = {}
        self._lock = asyncio.Lock()

    def seed_slots_for_day(self, day: date) -> None:
        """
        Сгенерируем слоты по 60 минут с 10:00 до 18:00 (можешь поменять под себя).
        """
        start_local = datetime(day.year, day.month, day.day, 10, 0, tzinfo=AMS)
        for i in range(8):  # 8 часов = 8 слотов
            s_local = start_local + timedelta(hours=i)
            e_local = s_local + timedelta(hours=1)
            s_utc = s_local.astimezone(ZoneInfo("UTC"))
            e_utc = e_local.astimezone(ZoneInfo("UTC"))
            sid = f"{day.isoformat()}-{i:02d}"
            self._slots.setdefault(sid, Slot(slot_id=sid, start_utc=s_utc, end_utc=e_utc))

    async def _available(self, slot_id: str) -> bool:
        # Слот свободен, если по нему нет брони
        for b in self._bookings.values():
            if b.slot_id == slot_id:
                return False
        return True

    async def list_slots_for_day(self, day: date) -> list[Slot]:
        self.seed_slots_for_day(day)
        return [s for s in self._slots.values() if s.start_utc.date() == day]

    async def create_booking(self, slot_id: str, name: str, email: str) -> Booking | None:
        async with self._lock:
            if slot_id not in self._slots:
                return None
            if not await self._available(slot_id):
                return None
            bid = uuid.uuid4().hex
            b = Booking(booking_id=bid, slot_id=slot_id, name=name, email=email)
            self._bookings[bid] = b
            return b

    async def cancel_booking(self, booking_id: str, email: str) -> bool:
        async with self._lock:
            b = self._bookings.get(booking_id)
            if not b or b.email.lower() != email.lower():
                return False
            del self._bookings[booking_id]
            return True

STORE = MemoryStore()
from __future__ import annotations

from datetime import datetime  # ✅ обязательный импорт!

from sqlalchemy.orm import (
    declarative_base,
    relationship,
    Mapped,
    mapped_column,
)
from sqlalchemy import String, DateTime, ForeignKey

Base = declarative_base()


class Slot(Base):
    __tablename__ = "slots"

    slot_id: Mapped[str] = mapped_column(String, primary_key=True)

    # ✅ тут используем datetime уже не в кавычках, потому что импортировали datetime
    start_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    end_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    bookings: Mapped[list["Booking"]] = relationship(
        "Booking", back_populates="slot", cascade="all, delete-orphan"
    )


class Booking(Base):
    __tablename__ = "bookings"

    booking_id: Mapped[str] = mapped_column(String, primary_key=True)
    slot_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("slots.slot_id"),
        index=True,
        nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)

    slot: Mapped[Slot] = relationship("Slot", back_populates="bookings")

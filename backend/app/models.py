"""SQLAlchemy ORM models for the Smart School Dismissal System."""

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class StudentStatus(str, enum.Enum):
    """Student pickup lifecycle status."""

    WAITING = "WAITING"
    ARRIVED = "ARRIVED"
    SENT_TO_GATE = "SENT_TO_GATE"
    PICKED_UP = "PICKED_UP"


class EventType(str, enum.Enum):
    """Pickup event type."""

    ARRIVED = "ARRIVED"
    SENT = "SENT"
    PICKED = "PICKED"


class EventSource(str, enum.Enum):
    """Source that triggered the event."""

    CAMERA = "CAMERA"
    APP = "APP"
    MANUAL = "MANUAL"


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _new_uuid() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class Student(Base):
    __tablename__ = "students"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=_new_uuid
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    grade: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[StudentStatus] = mapped_column(
        Enum(StudentStatus), nullable=False, default=StudentStatus.WAITING
    )
    pickup_person: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False
    )

    # Relationships
    cars: Mapped[list["Car"]] = relationship(back_populates="student")
    pickup_events: Mapped[list["PickupEvent"]] = relationship(
        back_populates="student"
    )

    def __repr__(self) -> str:
        return f"<Student {self.name} [{self.status.value}]>"


class Parent(Base):
    __tablename__ = "parents"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=_new_uuid
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )

    # Relationships
    cars: Mapped[list["Car"]] = relationship(back_populates="parent")

    def __repr__(self) -> str:
        return f"<Parent {self.name}>"


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=_new_uuid
    )
    plate_number: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False
    )
    parent_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("parents.id"), nullable=False
    )
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("students.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )

    # Relationships
    parent: Mapped["Parent"] = relationship(back_populates="cars")
    student: Mapped["Student"] = relationship(back_populates="cars")

    # Index on plate_number for fast lookups
    __table_args__ = (
        Index("ix_cars_plate_number", "plate_number"),
    )

    def __repr__(self) -> str:
        return f"<Car {self.plate_number}>"


class PickupEvent(Base):
    __tablename__ = "pickup_events"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=_new_uuid
    )
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("students.id"), nullable=False
    )
    event_type: Mapped[EventType] = mapped_column(
        Enum(EventType), nullable=False
    )
    source: Mapped[EventSource] = mapped_column(
        Enum(EventSource), nullable=False
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    student: Mapped["Student"] = relationship(back_populates="pickup_events")

    def __repr__(self) -> str:
        return f"<PickupEvent {self.event_type.value} for {self.student_id}>"

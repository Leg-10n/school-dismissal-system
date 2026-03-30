"""Pydantic schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import EventSource, EventType, StudentStatus


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


class HealthResponse(BaseModel):
    status: str = "healthy"
    database: str = "connected"


# ---------------------------------------------------------------------------
# Student
# ---------------------------------------------------------------------------


class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    grade: str = Field(..., min_length=1, max_length=50)
    pickup_person: str | None = None


class StudentUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    grade: str | None = Field(None, min_length=1, max_length=50)
    pickup_person: str | None = None


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    grade: str
    status: StudentStatus
    pickup_person: str | None
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# Parent
# ---------------------------------------------------------------------------


class ParentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    phone: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., max_length=255)


class ParentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    phone: str
    email: str
    created_at: datetime


# ---------------------------------------------------------------------------
# Car
# ---------------------------------------------------------------------------


class CarCreate(BaseModel):
    plate_number: str = Field(..., min_length=1, max_length=20)
    parent_id: str
    student_id: str


class CarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    plate_number: str
    parent_id: str
    student_id: str
    created_at: datetime


# ---------------------------------------------------------------------------
# Pickup Event
# ---------------------------------------------------------------------------


class PickupEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    student_id: str
    event_type: EventType
    source: EventSource
    timestamp: datetime
    notes: str | None

"""Pydantic models for API responses."""
from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(..., example="ok")


class PosTransaction(BaseModel):
    transaction_id: str
    store: str
    amount: float
    currency: str
    timestamp: datetime


class ReservationRecord(BaseModel):
    reservation_id: str
    restaurant: str
    party_size: int
    status: str
    reservation_time: datetime


class RevenueSummary(BaseModel):
    currency: str
    total_revenue: float
    average_ticket_size: float
    transaction_count: int


class OccupancyRate(BaseModel):
    restaurant: str
    confirmed_reservations: int
    cancelled_reservations: int
    average_party_size: float


class AnalyticsResponse(BaseModel):
    revenue: RevenueSummary
    occupancy: List[OccupancyRate]

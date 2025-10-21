"""FastAPI application exposing hospitality analytics."""
from __future__ import annotations

from typing import List

from fastapi import FastAPI

from .models import (
    AnalyticsResponse,
    HealthResponse,
    OccupancyRate,
    PosTransaction,
    ReservationRecord,
)
from .service import get_analytics, get_occupancy_rates
from .data_loader import load_pos_data, load_reservation_data

app = FastAPI(
    title="Hospitality Insights SaaS",
    description="Aggregated insights for restaurant groups combining POS and reservation data.",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Simple health check endpoint."""
    return HealthResponse(status="ok")


@app.get("/pos", response_model=List[PosTransaction])
def list_pos_transactions() -> List[PosTransaction]:
    """Return the POS transactions from all integrated vendors."""
    pos_df = load_pos_data()
    records = pos_df.to_dict(orient="records")
    return [PosTransaction(**record) for record in records]


@app.get("/reservations", response_model=List[ReservationRecord])
def list_reservations() -> List[ReservationRecord]:
    """Return the reservations across all connected reservation systems."""
    reservation_df = load_reservation_data()
    records = reservation_df.to_dict(orient="records")
    return [ReservationRecord(**record) for record in records]


@app.get("/analytics/revenue", response_model=AnalyticsResponse)
def get_revenue_and_occupancy() -> AnalyticsResponse:
    """Return revenue and occupancy analytics for the hospitality group."""
    return get_analytics()


@app.get("/analytics/occupancy", response_model=List[OccupancyRate])
def get_occupancy() -> List[OccupancyRate]:
    """Return only the occupancy metrics for each restaurant."""
    return get_occupancy_rates()


@app.get("/analytics/revenue/summary", response_model=AnalyticsResponse)
def get_revenue_only() -> AnalyticsResponse:
    """Return analytics with emphasis on revenue metrics."""
    return get_analytics()

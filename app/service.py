"""Business logic for the hospitality SaaS."""
from __future__ import annotations

import pandas as pd

from .data_loader import load_pos_data, load_reservation_data
from .models import AnalyticsResponse, OccupancyRate, RevenueSummary


def get_revenue_summary() -> RevenueSummary:
    pos_df = load_pos_data()
    if pos_df.empty:
        return RevenueSummary(
            currency="USD",
            total_revenue=0.0,
            average_ticket_size=0.0,
            transaction_count=0,
        )

    total_revenue = float(pos_df["amount"].sum())
    transaction_count = int(pos_df.shape[0])
    average_ticket = float(total_revenue / transaction_count) if transaction_count else 0.0
    currency = pos_df["currency"].mode().iat[0] if not pos_df["currency"].empty else "USD"

    return RevenueSummary(
        currency=currency,
        total_revenue=round(total_revenue, 2),
        average_ticket_size=round(average_ticket, 2),
        transaction_count=transaction_count,
    )


def get_occupancy_rates() -> list[OccupancyRate]:
    reservation_df = load_reservation_data()
    if reservation_df.empty:
        return []

    groups = reservation_df.groupby("restaurant")
    occupancy = []
    for restaurant, group in groups:
        confirmed = int((group["status"].str.lower() == "confirmed").sum())
        cancelled = int((group["status"].str.lower() == "cancelled").sum())
        avg_party = float(group["party_size"].mean()) if not group["party_size"].empty else 0.0
        occupancy.append(
            OccupancyRate(
                restaurant=restaurant,
                confirmed_reservations=confirmed,
                cancelled_reservations=cancelled,
                average_party_size=round(avg_party, 2),
            )
        )
    return sorted(occupancy, key=lambda record: record.restaurant)


def get_analytics() -> AnalyticsResponse:
    return AnalyticsResponse(
        revenue=get_revenue_summary(),
        occupancy=get_occupancy_rates(),
    )

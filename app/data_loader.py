"""Utility functions for loading POS and reservation data."""
from __future__ import annotations

from pathlib import Path
from typing import Literal

import pandas as pd

DATA_SOURCE_ROOT = Path(__file__).resolve().parent.parent / "samples"
POS_DATASET = DATA_SOURCE_ROOT / "pos"
RESERVATION_DATASET = DATA_SOURCE_ROOT / "reservation"


class DataSourceNotFoundError(FileNotFoundError):
    """Raised when a dataset cannot be located on disk."""


def _validate_dataset(path: Path, dataset_type: Literal["pos", "reservation"]) -> None:
    if not path.exists():
        raise DataSourceNotFoundError(
            f"The {dataset_type} dataset directory was not found at {path}."
        )


def load_pos_data() -> pd.DataFrame:
    """Return all available POS transactions as a DataFrame."""
    _validate_dataset(POS_DATASET, "pos")
    frames = []
    for csv_file in POS_DATASET.glob("*_sample.csv"):
        frames.append(pd.read_csv(csv_file))
    if not frames:
        return pd.DataFrame(columns=["transaction_id", "store", "amount", "currency", "timestamp"])
    return pd.concat(frames, ignore_index=True)


def load_reservation_data() -> pd.DataFrame:
    """Return all reservation data as a DataFrame."""
    _validate_dataset(RESERVATION_DATASET, "reservation")
    frames = []
    for csv_file in RESERVATION_DATASET.glob("*_sample.csv"):
        frames.append(pd.read_csv(csv_file))
    if not frames:
        return pd.DataFrame(columns=["reservation_id", "restaurant", "party_size", "status", "reservation_time"])
    return pd.concat(frames, ignore_index=True)

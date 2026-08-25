"""Shared project configuration for the notebook-centred workflow."""

from pathlib import Path


STUDY_START_YEAR = 2011
STUDY_END_YEAR = 2025
TRAIN_END_YEAR = 2022
TEST_START_YEAR = 2023
RANDOM_STATE = 42

# Semantic colours remain consistent across EDA and later analytical notebooks.
PROJECT_COLORS = {
    "housing": "#2F6B9A",
    "housing_light": "#B9D4E7",
    "climate": "#D95F0E",
    "disaster": "#B7410E",
    "nfip": "#C98900",
    "social": "#7A5195",
    "resilience": "#2A9D8F",
    "neutral": "#6B7280",
    "light_neutral": "#D1D5DB",
    "map_outline": "#F7F7F7",
}

PROJECT_CMAPS = {
    "housing": "Blues",
    "climate": "Oranges",
    "disaster": "YlOrRd",
    "nfip": "YlOrRd",
    "social": "Purples",
    "resilience": "Greens",
    "correlation": "RdBu_r",
}


def find_project_root(start_path=None):
    """Locate the repository root from a notebook or project subdirectory."""
    start = Path(start_path or Path.cwd()).resolve()
    for candidate in (start, *start.parents):
        if (candidate / "notebooks").is_dir() and (candidate / "data").is_dir():
            return candidate
    raise FileNotFoundError(
        "Could not locate the project root containing notebooks/ and data/."
    )

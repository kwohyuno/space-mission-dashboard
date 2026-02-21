"""
Space Missions Data Analysis Functions
8 functions for programmatic grading.
"""

import os
import pandas as pd

_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "space_missions.csv")


def _load_data() -> pd.DataFrame:
    """Load and parse the space missions CSV data."""
    df = pd.read_csv(_DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df


def getMissionCountByCompany(companyName: str) -> int:
    """Returns the total number of missions for a given company."""
    df = _load_data()
    return int((df["Company"] == companyName).sum())


def getSuccessRate(companyName: str) -> float:
    """Calculates the success rate for a given company as a percentage (0-100), rounded to 2 decimal places."""
    df = _load_data()
    company_missions = df[df["Company"] == companyName]
    if company_missions.empty:
        return 0.0
    successes = (company_missions["MissionStatus"] == "Success").sum()
    return round(float(successes / len(company_missions) * 100), 2)


def getMissionsByDateRange(startDate: str, endDate: str) -> list:
    """Returns mission names launched between startDate and endDate (inclusive), sorted chronologically."""
    df = _load_data()
    start = pd.to_datetime(startDate)
    end = pd.to_datetime(endDate)
    mask = (df["Date"] >= start) & (df["Date"] <= end)
    filtered = df[mask].sort_values("Date")
    return filtered["Mission"].tolist()


def getTopCompaniesByMissionCount(n: int) -> list:
    """Returns top N companies ranked by total number of missions.
    Returns list of tuples: [(companyName, missionCount), ...].
    Ties are broken alphabetically by company name.
    """
    df = _load_data()
    counts = df.groupby("Company").size().reset_index(name="count")
    counts = counts.sort_values(["count", "Company"], ascending=[False, True])
    return [(row["Company"], int(row["count"])) for _, row in counts.head(n).iterrows()]


def getMissionStatusCount() -> dict:
    """Returns the count of missions for each mission status."""
    df = _load_data()
    return {status: int(count) for status, count in df["MissionStatus"].value_counts().items()}


def getMissionsByYear(year: int) -> int:
    """Returns the total number of missions launched in a specific year."""
    df = _load_data()
    return int((df["Date"].dt.year == year).sum())


def getMostUsedRocket() -> str:
    """Returns the name of the most frequently used rocket.
    If multiple rockets are tied, returns the first one alphabetically.
    """
    df = _load_data()
    counts = df.groupby("Rocket").size().reset_index(name="count")
    max_count = counts["count"].max()
    top_rockets = counts[counts["count"] == max_count]
    return str(top_rockets.sort_values("Rocket").iloc[0]["Rocket"])


def getAverageMissionsPerYear(startYear: int, endYear: int) -> float:
    """Calculates the average number of missions per year over a given range (inclusive), rounded to 2 decimal places."""
    df = _load_data()
    num_years = endYear - startYear + 1
    if num_years <= 0:
        return 0.0
    mask = (df["Date"].dt.year >= startYear) & (df["Date"].dt.year <= endYear)
    total_missions = int(mask.sum())
    return round(float(total_missions / num_years), 2)

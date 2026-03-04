import asyncio
import functools
import os
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from noaa_cdo_api import Extent, NOAAClient

load_dotenv()

_original_make_request = NOAAClient._make_request


@functools.wraps(_original_make_request)
async def _patched_make_request(self, url, parameters=None, token_parameter=None):
    if parameters:
        parameters = {k: v for k, v in parameters.items() if v != ""}
    return await _original_make_request(self, url, parameters, token_parameter)


NOAAClient._make_request = _patched_make_request

# Config

NOAA_TOKEN = os.environ.get("NOAA_TOKEN")
if not NOAA_TOKEN:
    raise ValueError("NOAA_TOKEN environment variable not set")
OUTPUT_CSV = "../Data/Raw/Weather/Weather_data.csv"
INPUT_CSV = "../Data/Processed/05_Human_Readable.csv"

# Dundee Coords
DUNDEE_LAT = 56.4620
DUNDEE_LON = -2.9707

DATA_TYPES = ["TMAX", "TMIN", "PRCP"]


async def get_dundee_station(client):
    extent = Extent(
        DUNDEE_LAT - 0.1, DUNDEE_LON - 0.1, DUNDEE_LAT + 0.1, DUNDEE_LON + 0.1
    )

    stations = await client.get_stations(extent=extent, datasetid="GHCND", limit=1)
    if stations and stations.get("results"):
        return stations["results"][0]["id"]
    else:
        raise Exception("No weather station found near Dundee!")


async def fetch_all_weather(client, station_id, start_date, end_date):
    from datetime import timedelta

    all_results = []
    current_date = start_date
    one_year = timedelta(days=365)

    while current_date <= end_date:
        year_end = min(current_date + one_year - timedelta(days=1), end_date)
        print(f"Fetching {current_date} to {year_end}...")

        data = await client.get_data(
            datasetid="GHCND",
            stationid=station_id,
            startdate=current_date.strftime("%Y-%m-%d"),
            enddate=year_end.strftime("%Y-%m-%d"),
            datatypeid=DATA_TYPES,
            units="metric",
            limit=1000,
        )
        all_results.extend(data.get("results", []))
        current_date = year_end + timedelta(days=1)

    return all_results


def weather_by_date(weather_results):
    """Converts a list of weather results into a dict keyed by date."""
    # Structure: { date: {'TMAX': value, 'TMIN': value, 'PRCP': value} }
    daily = {}
    for item in weather_results:
        date_str = item["date"][:10]  # Extract YYYY-MM-DD from timestamp
        datatype = item["datatype"]
        value = item["value"]
        if date_str not in daily:
            daily[date_str] = {}
        daily[date_str][datatype] = value
    return daily


async def main():
    print("Loading CSV file...")
    df = pd.read_csv(INPUT_CSV)

    # Create a 'Date' column by combining Year, Month, Day
    df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]])

    # Find the overall date range needed
    start_date = df["Date"].min().date()
    end_date = df["Date"].max().date()
    print(f"Fetching weather from {start_date} to {end_date}")

    async with NOAAClient(token=NOAA_TOKEN) as client:
        # 1. Get station ID for Dundee
        station_id = await get_dundee_station(client)
        print(f"Using station: {station_id}")

        # 2. Fetch all weather data for the date range
        weather_results = await fetch_all_weather(
            client, station_id, start_date, end_date
        )
        print(f"Total records fetched: {len(weather_results)}")

        # 3. Organize by date
        daily_weather = weather_by_date(weather_results)

    # 4. Create standalone weather DataFrame with unique dates
    unique_dates = df["Date"].dt.date.unique()
    weather_df = pd.DataFrame()
    weather_df["Date"] = sorted(unique_dates)
    weather_df["Date"] = weather_df["Date"].astype(str)

    # 5. Add weather columns
    for dt in DATA_TYPES:
        weather_df[dt] = weather_df["Date"].map(lambda d: daily_weather.get(d, {}).get(dt))

    print("Saving weather CSV...")
    weather_df.to_csv(OUTPUT_CSV, index=False)
    print(f"Done! File saved to {OUTPUT_CSV}")


if __name__ == "__main__":
    asyncio.run(main())

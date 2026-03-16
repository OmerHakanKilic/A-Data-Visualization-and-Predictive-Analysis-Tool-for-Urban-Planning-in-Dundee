import pandas as pd


def main():
    weather_df = pd.read_csv("Data/Raw/Weather/Weather_data.csv")
    main_df = pd.read_csv("Data/Processed/06_With_Holidays.csv")

    weather_df["Date"] = pd.to_datetime(weather_df["Date"], format="%Y-%m-%d")
    weather_df["Year"] = weather_df["Date"].dt.year
    weather_df["Month"] = weather_df["Date"].dt.month
    weather_df["Day"] = weather_df["Date"].dt.day

    weather_cols = ["Year", "Month", "Day", "TMAX", "TMIN", "PRCP"]
    weather_df = weather_df[weather_cols]

    merged_df = main_df.merge(weather_df, on=["Year", "Month", "Day"], how="left")

    merged_df.to_csv("Data/Processed/07_weather_data_integrated.csv", index=False)
    print(f"Merged dataset saved with {len(merged_df)} rows")
    print(f"Weather data matched: {merged_df["TMAX"].notna().sum()} rows")


if __name__ == "__main__":
    main()

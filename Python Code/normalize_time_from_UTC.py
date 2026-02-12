import pandas as pd

target_file_path = "../Data/Processed/01_Merged_CCTV_data.csv"

target_file_df = pd.read_csv(target_file_path)

target_file_df.rename(columns={"Day": "Day of the Week"}, inplace=True)

date_utc = pd.to_datetime(target_file_df["Date"], utc=True)

local_dates = date_utc.dt.tz_convert("Europe/London")

target_file_df["Year"] = local_dates.dt.year
target_file_df["Month"] = local_dates.dt.month
target_file_df["Day"] = local_dates.dt.day
target_file_df["TimeZone"] = local_dates.dt.strftime("%Z")

target_file_df.drop(columns=["Date", "FID"], inplace=True)

print(target_file_df)

import pandas as pd

# Load your dataset
df = pd.read_csv("../Data/Processed/02_Time_Zone_Fixed.csv")


def convert_to_24h(time_str):
    """Converts a time string like '6:00 PM' to a numerical hour (18.0)."""
    try:
        # Use pandas to parse the time string into a datetime object
        dt = pd.to_datetime(time_str.strip(), format="%I:%M %p")
        # Return hour + minutes as a decimal for ML compatibility
        return dt.hour + dt.minute / 60.0
    except Exception:
        return None


# 1. Split the 'Hour' column into two strings at the '-' character
hour_split = df["Hour"].str.split("-", expand=True)

# 2. Apply the conversion function to both parts
df["Starting time"] = hour_split[0].apply(convert_to_24h)
df["Finishing time"] = hour_split[1].apply(convert_to_24h)

df.drop(columns=["Hour"], inplace=True)

# 3. Save the processed data
df.to_csv("../Data/Processed/03_Processed_Time_Data.csv", index=False)

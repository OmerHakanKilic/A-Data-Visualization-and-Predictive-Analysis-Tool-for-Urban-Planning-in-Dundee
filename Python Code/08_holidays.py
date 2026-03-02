import pandas as pd

df = pd.read_csv("../Data/Raw/Holidays/2023-24-25.csv")

df["Date"] = df["Date"].str.replace("*", "", regex=False)

df["Date"] = pd.to_datetime(df["Date"], format="%d %B %Y")

df["DayOfWeek"] = df["Day"]

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Day"] = df["Date"].dt.day

output_df = df[["Year", "Month", "Day", "DayOfWeek", "Holiday"]].copy()
output_df.columns = ["Year", "Month", "Day", "Day of Week", "Holiday"]

output_df.to_csv("../Data/Processed/Holidays_Processed.csv", index=False)

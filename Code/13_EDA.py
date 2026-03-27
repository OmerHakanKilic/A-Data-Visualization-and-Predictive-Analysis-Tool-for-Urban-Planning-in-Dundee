import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv("../Data/Processed/07_weather_data_integrated.csv")

print(df.head())  # first 5 rows
print("############################################################################")
print(df.info())  # data types, non‑null counts
print("############################################################################")
print(df.describe(include="all"))  # extended stats for all columns
print("############################################################################")

# Number of People Histogram
sns.histplot(data=df, x="Number of People", kde=True)
plt.title("Distribution of Target")
plt.show()

# Number of Vehicles Histogram
sns.histplot(data=df, x="Number of Road Vehicles", kde=True)
plt.title("Distribution of Target")
plt.show()

# Number of Bicycles Histogram
sns.histplot(data=df, x="Number of Bicycles", kde=True)
plt.title("Distribution of Target")
plt.show()

# Line graphs - Daily trends
df_copy = df.copy()
df_copy["date"] = pd.to_datetime(
    df_copy["Year"].astype(str) + "-" + 
    df_copy["Month"].astype(str).str.zfill(2) + "-" + 
    df_copy["Day"].astype(str).str.zfill(2)
)

daily_totals = df_copy.groupby("date").agg({
    "Number of People": "sum",
    "Number of Road Vehicles": "sum",
    "Number of Bicycles": "sum"
}).reset_index()

plt.figure(figsize=(12, 5))
plt.plot(daily_totals["date"], daily_totals["Number of People"], marker="o")
plt.title("Daily Total - Number of People")
plt.xlabel("Date")
plt.ylabel("Number of People")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 5))
plt.plot(daily_totals["date"], daily_totals["Number of Road Vehicles"], marker="o", color="orange")
plt.title("Daily Total - Number of Road Vehicles")
plt.xlabel("Date")
plt.ylabel("Number of Road Vehicles")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 5))
plt.plot(daily_totals["date"], daily_totals["Number of Bicycles"], marker="o", color="green")
plt.title("Daily Total - Number of Bicycles")
plt.xlabel("Date")
plt.ylabel("Number of Bicycles")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

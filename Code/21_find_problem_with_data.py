import matplotlib.pyplot as plt
import pandas as pd

df_2024 = pd.read_csv("../Data/Raw/CCTV-Data/CCTV_Data_Counts_January_2024.csv")
print(df_2024.describe())
df_2025 = pd.read_csv("../Data/Raw/CCTV-Data/CCTV_Data_Counts_August_2024.csv")
print(df_2025.describe())
df_2024["datetime"] = pd.to_datetime(df_2024["Date"]) + pd.to_timedelta(
    df_2024["Hour"]
    .str.split("-")
    .str[0]
    .str.strip()
    .apply(
        lambda x: int(x.split(":")[0])
        + (12 if "PM" in x and "12" not in x.split(":")[0] else 0)
        - (12 if "AM" in x and x.split(":")[0] == "12" else 0)
    ),
    unit="h",
)

df_2025["datetime"] = pd.to_datetime(df_2025["Date"]) + pd.to_timedelta(
    df_2025["Hour"]
    .str.split("-")
    .str[0]
    .str.strip()
    .apply(
        lambda x: int(x.split(":")[0])
        + (12 if "PM" in x and "12" not in x.split(":")[0] else 0)
        - (12 if "AM" in x and x.split(":")[0] == "12" else 0)
    ),
    unit="h",
)

plt.figure(figsize=(14, 6))
plt.scatter(
    df_2024["datetime"], df_2024["Number_of_People"], label="January 2024", alpha=0.7
)
plt.scatter(
    df_2025["datetime"], df_2025["F__of_People"], label="February 2025", alpha=0.7
)
plt.xlabel("Date + Hour")
plt.ylabel("Number of People")
plt.title("Number of People: January 2024 vs February 2025")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

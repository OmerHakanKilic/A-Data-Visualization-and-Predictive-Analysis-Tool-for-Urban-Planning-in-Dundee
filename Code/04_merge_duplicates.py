import pandas as pd

# Load the previously processed dataset
df = pd.read_csv("../Data/Processed/03_Processed_Time_Data.csv")

# 1. Define the groups of columns to merge
bicycle_cols = ["F__of_Bicycles", "Number_of_Bicycles", "Number_of_Bicycles_"]
people_cols = ["F__of_People", "Number_of_People"]
vehicle_cols = [
    "F__of_Road_Vehicles",
    "Number_of_Road_Vehicles",
    "Number_of_Road_Vehicles_",
]

# 2. Merge the columns
# .sum(axis=1) adds the values across the columns for each row
# min_count=1 ensures that if all columns are NaN, the result is NaN (not 0)
df["Number of Bicycles"] = df[bicycle_cols].sum(axis=1, min_count=1)
df["Number of People"] = df[people_cols].sum(axis=1, min_count=1)
df["Number of Road Vehicles"] = df[vehicle_cols].sum(axis=1, min_count=1)

# 3. Drop the original redundant columns
cols_to_drop = bicycle_cols + people_cols + vehicle_cols
df.drop(columns=cols_to_drop, inplace=True)

# Save the final cleaned dataset
df.to_csv("../Data/Processed/04_Merged_Duplicates.csv", index=False)

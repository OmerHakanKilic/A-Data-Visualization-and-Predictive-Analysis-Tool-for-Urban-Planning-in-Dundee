import pandas as pd

df = pd.read_csv("../Data/Processed/04_Merged_Duplicates.csv")

# Define the columns that should be whole numbers
target_columns = [
    "Starting time",
    "Finishing time",
    "Number of Bicycles",
    "Number of People",
    "Number of Road Vehicles",
]

# Convert them all at once using astype
df[target_columns] = df[target_columns].astype(int)

df.to_csv("../Data/Processed/05_Human_Readable.csv", index=False)

import os
import pandas as pd

INPUT_PATH = "../Data/Processed/09_data_encoded.csv"
OUTPUT_PATH = "../Data/Processed/20_days_since_record.csv"


def main():
    df = pd.read_csv(INPUT_PATH)

    df["days_since_record"] = 0

    df.loc[
        (df["Year"] == 2024) & (df["Month"] == 7) & (df["Day"] == 1),
        "days_since_record",
    ] = 90

    df.loc[
        (df["Year"] == 2024) & (df["Month"] == 12) & (df["Day"] == 1),
        "days_since_record",
    ] = 60

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

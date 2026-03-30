import os
from datetime import datetime

import pandas as pd

INPUT_DATA_PATH = "../Data/Processed/20_days_since_record.csv"
SPLIT_DATE = datetime(2024, 8, 1)

TARGETS = [
    "Number of Bicycles",
    "Number of People",
    "Number of Road Vehicles",
]

OUTPUT_FILES = {
    "Number of Bicycles": {
        "train": "../Data/Processed/12_train_bicycles_for_prophet.csv",
        "test": "../Data/Processed/13_test_bicycles_for_prophet.csv",
    },
    "Number of People": {
        "train": "../Data/Processed/14_train_people_for_prophet.csv",
        "test": "../Data/Processed/15_test_people_for_prophet.csv",
    },
    "Number of Road Vehicles": {
        "train": "../Data/Processed/16_train_vehicles_for_prophet.csv",
        "test": "../Data/Processed/17_test_vehicles_for_prophet.csv",
    },
}


def prepare_prophet_data(
    df: pd.DataFrame, target: str, split_date: datetime
) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = df.copy()

    df["ds"] = pd.to_datetime(
        df["Year"].astype(str)
        + "-"
        + df["Month"].astype(str).str.zfill(2)
        + "-"
        + df["Day"].astype(str).str.zfill(2)
        + " "
        + df["Starting time"].astype(str).str.zfill(2)
        + ":00:00"
    )

    feature_cols = [col for col in df.columns if col not in ["ds", target]]

    train_df = df[df["ds"] < split_date][["ds", target] + feature_cols].copy()
    test_df = df[df["ds"] >= split_date][["ds", target] + feature_cols].copy()

    train_df = train_df.rename(columns={target: "y"})
    test_df = test_df.rename(columns={target: "y"})

    train_df = train_df.sort_values("ds").reset_index(drop=True)
    test_df = test_df.sort_values("ds").reset_index(drop=True)

    return train_df, test_df


def main() -> None:
    print(f"Loading data from {INPUT_DATA_PATH}...")
    df = pd.read_csv(INPUT_DATA_PATH)
    print(f"Loaded {len(df)} rows")

    for target in TARGETS:
        print(f"\nProcessing target: {target}")
        train_df, test_df = prepare_prophet_data(df, target, SPLIT_DATE)

        train_path = OUTPUT_FILES[target]["train"]
        test_path = OUTPUT_FILES[target]["test"]

        train_df.to_csv(train_path, index=False)
        test_df.to_csv(test_path, index=False)

        print(f"  Train: {len(train_df)} rows -> {train_path}")
        print(f"  Test:  {len(test_df)} rows -> {test_path}")

    print("\nDone!")


if __name__ == "__main__":
    main()

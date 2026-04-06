from datetime import datetime

import pandas as pd

INPUT_DATA_PATH = "../Data/Processed/20_days_since_record.csv"
OUTPUT_DIRECTORY_PATH = "../Data/Output/Prophetv2/"
SPLIT_DATE = datetime(2024, 8, 1)

TARGETS = [
    "Number of Bicycles",
    "Number of People",
    "Number of Road Vehicles",
]

CAMERA_COLUMNS = [
    "Source_Camera  308 Murraygate",
    "Source_Camera 310 - Seagate",
    "Source_Camera 317 Reform St",
    "Source_Camera 320 Westport",
    "Source_Camera 323 Union Street",
    "Source_Camera 328 South Marketgait",
    "Source_Camera 331 Railway Station",
    "Source_Camera 332 Waterfront",
    "Source_Camera 500 Hilltown",
]


def get_camera_name(col: str) -> str:
    return (
        col.replace("Source_Camera", "")
        .replace("  ", " ")
        .strip()
        .replace(" - ", "_")
        .replace(" ", "_")
        .lower()
    )


def combine_date(row: pd.Series) -> datetime:
    return datetime(
        int(row["Year"]),
        int(row["Month"]),
        int(row["Day"]),
        int(row["Starting time"]),
    )


def process_camera_data(
    df: pd.DataFrame, camera_col: str, target: str
) -> tuple[pd.DataFrame, pd.DataFrame]:
    camera_df = df[df[camera_col] == 1].copy()

    camera_df = camera_df.drop(columns=CAMERA_COLUMNS, errors="ignore")

    if "Source_Camera" in camera_df.columns:
        camera_df = camera_df.drop(columns=["Source_Camera"])

    camera_df["ds"] = camera_df.apply(combine_date, axis=1)
    camera_df = camera_df.rename(columns={target: "y"})

    feature_cols = ["ds", "y"] + [
        c for c in camera_df.columns if c not in ["ds", "y", "Year", "Month", "Day", "Starting time"]
    ]
    camera_df = camera_df[feature_cols]

    train_df = camera_df[camera_df["ds"] < SPLIT_DATE].copy()
    test_df = camera_df[camera_df["ds"] >= SPLIT_DATE].copy()

    return train_df, test_df


def main():
    df = pd.read_csv(INPUT_DATA_PATH)

    for camera_col in CAMERA_COLUMNS:
        camera_name = get_camera_name(camera_col)

        for target in TARGETS:
            target_slug = target.replace(" ", "_").lower()

            train_df, test_df = process_camera_data(df, camera_col, target)

            train_filename = f"{camera_name}_{target_slug}_train.csv"
            test_filename = f"{camera_name}_{target_slug}_test.csv"

            train_path = OUTPUT_DIRECTORY_PATH + train_filename
            test_path = OUTPUT_DIRECTORY_PATH + test_filename

            train_df.to_csv(train_path, index=False)
            test_df.to_csv(test_path, index=False)

            print(f"Created: {train_filename} ({len(train_df)} rows)")
            print(f"Created: {test_filename} ({len(test_df)} rows)")


if __name__ == "__main__":
    main()

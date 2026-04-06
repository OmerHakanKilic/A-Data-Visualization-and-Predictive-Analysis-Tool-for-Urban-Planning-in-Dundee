import os
import re

import matplotlib.pyplot as plt
import pandas as pd

DATA_DIR = "../Data/Raw/CCTV-Data"


def parse_datetime(df: pd.DataFrame) -> pd.DataFrame:
    df["datetime"] = pd.to_datetime(df["Date"]) + pd.to_timedelta(
        df["Hour"]
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
    return df


def get_count_column(df: pd.DataFrame) -> str:
    for col in ["Number_of_People", "F__of_People", "Count"]:
        if col in df.columns:
            return col
    raise ValueError(f"No count column found in {df.columns}")


def main():
    csv_files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith(".csv")])
    print(f"Found {len(csv_files)} CSV files")

    month_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    colors = plt.cm.tab20(range(20))

    def get_label_and_color(csv_file: str, color_idx: int) -> tuple:
        match = re.search(r"(\w+)_(\d{4})\.csv$", csv_file)
        if match:
            month, year = match.groups()
            return f"{month} {year}", color_idx
        match = re.search(r"CCTV_Data_Counts_(\d{4})_(\w+)\.csv$", csv_file)
        if match:
            year, month = match.groups()
            return f"{month} {year}", color_idx
        match = re.search(r"Test_Counts_(\w+)(\d{2})\.csv$", csv_file)
        if match:
            month, year = match.groups()
            year = f"20{year}"
            return f"{month} {year}", color_idx
        return None, None

    plt.figure(figsize=(16, 8))

    for color_idx, csv_file in enumerate(csv_files):
        filepath = os.path.join(DATA_DIR, csv_file)
        label, _ = get_label_and_color(csv_file, color_idx)
        if label is None:
            print(f"Skipping {csv_file}: could not parse month/year")
            continue

        color = colors[color_idx % 20]

        df = pd.read_csv(filepath)
        count_col = get_count_column(df)
        df = parse_datetime(df)

        plt.scatter(
            df["datetime"], df[count_col], label=label, color=color, alpha=0.7, s=20
        )

    plt.xlabel("Date + Hour")
    plt.ylabel("Number of People")
    plt.title("Number of People by Month")
    plt.legend(loc="upper right", fontsize=8, ncol=2)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("output_visualization.png", dpi=150)
    print("Saved plot to output_visualization.png")


if __name__ == "__main__":
    main()
import pandas as pd

INPUT_PATH = "../Data/Processed/07_weather_data_integrated.csv"
OUTPUT_PATH = "../Data/Processed/08_weather_data_imputted.csv"

COLUMNS_TO_IMPUTE = ["TMAX", "TMIN", "PRCP"]


def main():
    df = pd.read_csv(INPUT_PATH)

    print(f"Loaded {len(df)} rows")
    print(f"Missing values before imputation:")
    for col in COLUMNS_TO_IMPUTE:
        missing_count = df[col].isna().sum()
        print(f"  {col}: {missing_count}")

    for col in COLUMNS_TO_IMPUTE:
        median_value = df[col].median()
        df[col] = df[col].fillna(median_value)
        print(f"Imputed {col} with median: {median_value}")

    print(f"\nMissing values after imputation:")
    for col in COLUMNS_TO_IMPUTE:
        missing_count = df[col].isna().sum()
        print(f"  {col}: {missing_count}")

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

import os
import re
from datetime import datetime
from glob import glob

import joblib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_squared_error

DATA_DIR = "../Data/Output/Prophetv3/"
OUTPUT_DIR = "../Output/prophetv3/"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_model_name_from_filename(filename: str) -> str:
    return filename.replace("_train.csv", "")


def get_feature_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c not in ["ds", "y"]]


def train_and_evaluate(train_path: str, test_path: str, model_name: str) -> float:
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    feature_cols = get_feature_columns(train_df)

    train_prophet = train_df[["ds", "y"]].copy()
    for col in feature_cols:
        train_prophet[col] = train_df[col]

    model = Prophet()
    for col in feature_cols:
        model.add_regressor(col)

    model.fit(train_prophet)

    model_path = os.path.join(OUTPUT_DIR, f"{model_name}.joblib")
    joblib.dump(model, model_path)

    train_forecast = model.predict(train_prophet)
    train_forecast["yhat"] = np.maximum(0, train_forecast["yhat"]).astype(int)
    train_df = train_df.copy()
    train_df["predicted"] = train_forecast["yhat"].values

    if len(test_df) == 0:
        return float("nan")

    test_prophet = test_df[["ds"]].copy()
    for col in feature_cols:
        test_prophet[col] = test_df[col]

    forecast = model.predict(test_prophet)
    forecast["yhat"] = np.maximum(0, forecast["yhat"]).astype(int)
    test_df = test_df.copy()
    test_df["predicted"] = forecast["yhat"].values

    plot_prediction(train_df, test_df, model_name)

    rmse = mean_squared_error(test_df["y"], test_df["predicted"]) ** 0.5

    return rmse


def plot_prediction(train_df: pd.DataFrame, test_df: pd.DataFrame, model_name: str):
    train_df = train_df.copy()
    test_df = test_df.copy()

    train_df["ds"] = pd.to_datetime(train_df["ds"])
    test_df["ds"] = pd.to_datetime(test_df["ds"])

    train_df = train_df.sort_values("ds")
    test_df = test_df.sort_values("ds")

    plt.figure(figsize=(12, 6))
    plt.plot(
        train_df["ds"], train_df["y"], label="Train Actual", color="blue", alpha=0.7
    )
    plt.plot(
        train_df["ds"],
        train_df["predicted"],
        label="Train Predicted",
        color="orange",
        alpha=0.7,
    )
    plt.plot(test_df["ds"], test_df["y"], label="Test Actual", color="green", alpha=0.7)
    plt.plot(
        test_df["ds"],
        test_df["predicted"],
        label="Test Predicted",
        color="red",
        alpha=0.7,
    )
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.title(f"Predictions vs Actuals - {model_name}")
    plt.legend()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)
    plt.tight_layout()

    plot_path = os.path.join(OUTPUT_DIR, f"{model_name}_prediction.png")
    plt.savefig(plot_path)
    plt.close()


def main():
    train_files = sorted(glob(os.path.join(DATA_DIR, "*_train.csv")))

    results = []

    for train_path in train_files:
        filename = os.path.basename(train_path)
        model_name = get_model_name_from_filename(filename)
        test_path = train_path.replace("_train.csv", "_test.csv")

        print(f"Training model: {model_name}")

        rmse = train_and_evaluate(train_path, test_path, model_name)
        results.append((model_name, rmse))

        print(f"  RMSE: {rmse:.4f}" if not pd.isna(rmse) else "  No test data")

    with open(os.path.join(OUTPUT_DIR, "rmse_results.txt"), "w") as f:
        f.write("Model,RMSE\n")
        for model_name, rmse in results:
            if pd.isna(rmse):
                f.write(f"{model_name},NA\n")
            else:
                f.write(f"{model_name},{rmse:.4f}\n")

    print(f"\nResults saved to {OUTPUT_DIR}rmse_results.txt")


if __name__ == "__main__":
    main()

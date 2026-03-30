import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from prophet import Prophet

OUTPUT_DIR = Path("../Output/Prophet")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DATA_FILES = {
    "bicycles": {
        "train": "../Data/Processed/12_train_bicycles_for_prophet.csv",
        "test": "../Data/Processed/13_test_bicycles_for_prophet.csv",
    },
    "people": {
        "train": "../Data/Processed/14_train_people_for_prophet.csv",
        "test": "../Data/Processed/15_test_people_for_prophet.csv",
    },
    "vehicles": {
        "train": "../Data/Processed/16_train_vehicles_for_prophet.csv",
        "test": "../Data/Processed/17_test_vehicles_for_prophet.csv",
    },
}

COLS_TO_DROP = [
    "Year",
    "Month",
    "Day",
    "Starting time",
    "Finishing time",
    "Day of the Week_Fri",
    "Day of the Week_Mon",
    "Day of the Week_Sat",
    "Day of the Week_Sun",
    "Day of the Week_Thu",
    "Day of the Week_Tue",
    "Day of the Week_Wed",
    "TimeZone_BST",
    "TimeZone_GMT",
    "Number of Bicycles",
    "Number of People",
    "Number of Road Vehicles",
]


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    mae = np.mean(np.abs(y_true - y_pred))
    rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
    mape = np.mean(np.abs((y_true - y_pred) / np.where(y_true == 0, 1, y_true))) * 100
    return {"MAE": mae, "RMSE": rmse, "MAPE": mape}


def train_and_evaluate(
    name: str, train_path: str, test_path: str
) -> None:
    print(f"\n{'=' * 50}")
    print(f"Processing: {name}")
    print("=" * 50)

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    drop_cols = [col for col in COLS_TO_DROP if col in train_df.columns]
    feature_cols = [col for col in train_df.columns if col not in ["ds", "y"] + drop_cols]

    print(f"Using {len(feature_cols)} regressors: {feature_cols}")

    train_prophet = train_df[["ds", "y"] + feature_cols].copy()

    model = Prophet()
    for col in feature_cols:
        model.add_regressor(col)

    print("Training model...")
    model.fit(train_prophet)

    model_path = OUTPUT_DIR / f"{name}_model.joblib"
    joblib.dump(model, model_path)
    print(f"Saved model: {model_path}")

    test_prophet = test_df[["ds"] + feature_cols].copy()
    forecast = model.predict(test_prophet)

    predictions_df = pd.DataFrame({
        "ds": test_df["ds"],
        "y_true": test_df["y"],
        "y_pred": forecast["yhat"],
    })
    predictions_path = OUTPUT_DIR / f"{name}_predictions.csv"
    predictions_df.to_csv(predictions_path, index=False)
    print(f"Saved predictions: {predictions_path}")

    metrics = calculate_metrics(
        test_df["y"].values, forecast["yhat"].values
    )

    metrics_path = OUTPUT_DIR / f"{name}_metrics.txt"
    with open(metrics_path, "w") as f:
        f.write(f"Model: {name}\n")
        f.write(f"Test samples: {len(test_df)}\n")
        f.write(f"MAE:  {metrics['MAE']:.4f}\n")
        f.write(f"RMSE: {metrics['RMSE']:.4f}\n")
        f.write(f"MAPE: {metrics['MAPE']:.4f}%\n")
    print(f"Saved metrics: {metrics_path}")
    print(f"MAE: {metrics['MAE']:.4f}, RMSE: {metrics['RMSE']:.4f}, MAPE: {metrics['MAPE']:.2f}%")


def save_plots() -> None:
    print("\nGenerating prediction plots...")
    
    model_names = ["bicycles", "people", "vehicles"]
    fig, axes = plt.subplots(3, 1, figsize=(20, 18))
    
    sns.set_style("darkgrid")
    
    for idx, name in enumerate(model_names):
        pred_path = OUTPUT_DIR / f"{name}_predictions.csv"
        df = pd.read_csv(pred_path)
        df["ds"] = pd.to_datetime(df["ds"])
        
        ax = axes[idx]
        
        sns.lineplot(data=df, x="ds", y="y_true", ax=ax, label="Actual", color="blue", alpha=0.7)
        sns.lineplot(data=df, x="ds", y="y_pred", ax=ax, label="Predicted", color="orange", alpha=0.7)
        
        ax.set_title(f"{name.title()} - Actual vs Predicted", fontsize=14, fontweight="bold")
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Count", fontsize=12)
        ax.legend(fontsize=10)
    
    plt.tight_layout()
    
    plot_path = OUTPUT_DIR / "comparison_plot.png"
    plt.savefig(plot_path, dpi=150, bbox_inches="tight")
    plt.close()
    
    print(f"Saved plot: {plot_path}")


def main() -> None:
    print("Prophet Model Training")
    print("=" * 50)

    for name, paths in DATA_FILES.items():
        train_and_evaluate(name, paths["train"], paths["test"])

    save_plots()

    print("\n" + "=" * 50)
    print("All models trained successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 50)


if __name__ == "__main__":
    main()

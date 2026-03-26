from pathlib import Path

import numpy as np
import pandas as pd
from joblib import dump
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

TRAINING_PATH = "../Data/Processed/10_training_before_regularization.csv"
TESTING_PATH = "../Data/Processed/11_testing_before_regularization.csv"
OUTPUT_DIR = Path("../Output/")

TARGETS = [
    "Number of Bicycles",
    "Number of People",
    "Number of Road Vehicles",
]


def evaluate_and_print(model: LinearRegression, X, y_true, label: str) -> dict:
    # Prediction with clamping to zero and rounding down
    y_pred = np.floor(np.maximum(0, model.predict(X)))
    # Mean absolute error eval
    mae = mean_absolute_error(y_true, y_pred)
    # Root mean squared error eval
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    # R squared eval
    r2 = r2_score(y_true, y_pred)

    print(f"  {label:10s} | MAE: {mae:8.2f} | RMSE: {rmse:8.2f} | R²: {r2:.4f}")
    return {"mae": mae, "rmse": rmse, "r2": r2, "predictions": y_pred}


def main():
    train_df = pd.read_csv(TRAINING_PATH)
    test_df = pd.read_csv(TESTING_PATH)
    print(f"Training: {len(train_df):,} rows | Testing: {len(test_df):,} rows\n")

    results = {}
    for target in TARGETS:
        print(f"=== {target} ===")

        y_train = train_df[target]
        y_test = test_df[target]
        X_train = train_df.drop(columns=TARGETS)
        X_test = test_df.drop(columns=TARGETS)

        model = LinearRegression()
        model.fit(X_train, y_train)

        train_metrics = evaluate_and_print(model, X_train, y_train, "Train")
        test_metrics = evaluate_and_print(model, X_test, y_test, "Test")

        base_name = target.lower().replace(" ", "_")
        model_path = OUTPUT_DIR / f"model_{base_name}.pkl"
        train_pred_path = OUTPUT_DIR / f"predictions_train_{base_name}.csv"
        test_pred_path = OUTPUT_DIR / f"predictions_test_{base_name}.csv"

        # Save the model to the path
        dump(model, model_path)

        pd.DataFrame(
            {"actual": y_train, "predicted": train_metrics["predictions"]}
        ).to_csv(train_pred_path, index=False)

        pd.DataFrame(
            {"actual": y_test, "predicted": test_metrics["predictions"]}
        ).to_csv(test_pred_path, index=False)

        print(
            f"  Saved: {model_path.name}, {train_pred_path.name}, {test_pred_path.name}\n"
        )
        results[target] = {"train": train_metrics, "test": test_metrics}

    print("=" * 60)
    print(f"{'Target':<25} {'MAE':>10} {'RMSE':>10} {'R²':>10}")
    print("-" * 60)

    for target, metrics in results.items():
        m = metrics["test"]
        print(f"{target:<25} {m['mae']:>10.2f} {m['rmse']:>10.2f} {m['r2']:>10.4f}")
    print("=" * 60)


if __name__ == "__main__":
    main()

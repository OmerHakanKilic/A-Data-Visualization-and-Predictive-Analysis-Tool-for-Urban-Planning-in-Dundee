from typing import cast

import pandas as pd
from sklearn.model_selection import train_test_split

TRAINING_RATIO = 0.8
TESTING_RATIO = 0.2

INPUT_PATH = "../Data/Processed/09_data_encoded.csv"
TRAINING_OUTPUT = "../Data/Processed/10_training_before_regularization.csv"
TESTING_OUTPUT = "../Data/Processed/11_testing_before_regularization.csv"

df = pd.read_csv(INPUT_PATH)
print(f"Loaded {len(df):,} rows from {INPUT_PATH}")

train_df, test_df = cast(
    tuple[pd.DataFrame, pd.DataFrame],
    train_test_split(
        df,
        train_size=TRAINING_RATIO,
        test_size=TESTING_RATIO,
        random_state=42,
    ),
)

train_df.to_csv(TRAINING_OUTPUT, index=False)
test_df.to_csv(TESTING_OUTPUT, index=False)

print(f"Training: {len(train_df):,} rows saved to {TRAINING_OUTPUT}")
print(f"Testing:  {len(test_df):,} rows saved to {TESTING_OUTPUT}")
print(f"Ratio:    {len(train_df)/len(df)*100:.1f}% / {len(test_df)/len(df)*100:.1f}%")

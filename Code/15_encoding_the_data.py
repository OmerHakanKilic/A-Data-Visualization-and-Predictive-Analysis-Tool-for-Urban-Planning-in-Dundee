import pandas as pd

input_df = pd.read_csv("../Data/Processed/08_weather_data_imputted.csv")

output_address = "../Data/Processed/09_data_encoded.csv"

FEATURES_TO_ENCODE = ["Day of the Week", "Source", "TimeZone"]

encoded_df = pd.get_dummies(input_df, columns=FEATURES_TO_ENCODE, dtype=int)

encoded_df.to_csv(output_address, index=False)

print(f"Encoded {len(FEATURES_TO_ENCODE)} columns: {FEATURES_TO_ENCODE}")
print(f"Original shape: {input_df.shape}")
print(f"Encoded shape: {encoded_df.shape}")
print(f"Saved to: {output_address}")

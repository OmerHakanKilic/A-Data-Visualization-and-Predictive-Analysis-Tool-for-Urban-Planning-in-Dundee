import glob
import os

import pandas as pd

target_csv_folder = "../Data/Raw/CCTV-Data"

# Get a list of csv files
csv_files = glob.glob(os.path.join(target_csv_folder, "*.csv"))

list_of_df_from_csv_files = [pd.read_csv(filename) for filename in csv_files]

merged_df = pd.concat(list_of_df_from_csv_files, ignore_index=True)

merged_df.to_csv("../Data/Processed/01_Merged_CCTV_data.csv", index=False)

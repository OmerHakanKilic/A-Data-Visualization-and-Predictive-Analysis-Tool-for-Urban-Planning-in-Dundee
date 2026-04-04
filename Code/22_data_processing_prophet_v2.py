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

LIST_OF_SOURCE_CAMERA = []

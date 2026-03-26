# AGENTS.md - Big Data Project Development Guide

This document provides guidance for agentic coding agents working in this repository.

## Project Overview

This is a Big Data educational project focused on processing and visualizing CCTV data from Dundee, Scotland. The codebase consists of Python scripts for data processing and a PyQt6-based GUI application for map visualization.

## Project Structure

```
Big Data/
├── Code/                    # All Python scripts and applications
│   ├── 01_merge_csv_script.py
│   ├── 02_normalize_time_from_UTC.py
│   ├── 03_reformat_time.py
│   ├── 04_merge_duplicates.py
│   ├── 05_convert_floats_to_int.py
│   ├── 08_holidays.py
│   ├── 09_add_holiday_flag.py
│   ├── 10_fetch_weather_data.py
│   ├── 11_map_demo_refined.py   # PyQt6 app with histograms
│   ├── 12_add_weather_data_to_dataset.py
│   ├── 13_EDA.py
│   ├── 14_handling_missing_values.py
│   ├── 15_encoding_the_data.py
│   ├── 16_splitting_data.py
│   ├── 06_tab_demo.py        # PyQt6 demo (tab navigation)
│   └── 07_map_demo.py        # Main PyQt6 map visualization app
├── Data/
│   ├── Raw/                 # Raw input data (CCTV-Data, Holidays, Weather)
│   └── Processed/           # Processed output data
├── Output/                  # Generated output files
└── Documents/               # Project documentation (sensitive)
```

## Build and Runtime Commands

### Running Python Scripts

Execute data processing scripts in order (they depend on previous outputs):

```bash
cd Code/
python 01_merge_csv_script.py
python 02_normalize_time_from_UTC.py
python 03_reformat_time.py
python 04_merge_duplicates.py
python 05_convert_floats_to_int.py
python 08_holidays.py
python 09_add_holiday_flag.py
python 10_fetch_weather_data.py
python 12_add_weather_data_to_dataset.py
python 13_EDA.py
python 14_handling_missing_values.py
python 15_encoding_the_data.py
python 16_splitting_data.py
```

### Running GUI Applications

```bash
python Code/11_map_demo_refined.py   # Main map visualization with histograms
python Code/07_map_demo.py          # Basic map demo
python Code/06_tab_demo.py           # PyQt6 tab demo
```

## Dependencies

```bash
pip install pandas matplotlib numpy PyQt6 noaa-cdo-api aiohttp python-dotenv
```

## Linting and Code Quality

```bash
pip install ruff black mypy
black Code/          # Format code
ruff check Code/     # Lint code
mypy Code/           # Type checking
```

## Code Style Guidelines

### Python Version & Formatting

- Target Python 3.9+, use f-strings, max line length: 100, 4 spaces for indentation
- Blank lines between top-level definitions, trailing commas for multi-line collections
- Always use `if __name__ == "__main__":` guard for executable scripts

### Imports

Standard library first, then third-party. Use explicit imports (no `from module import *`), sort alphabetically within groups:

```python
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QMainWindow,
    QWidget,
)
```

### Naming Conventions

- **Classes:** PascalCase (`MapPage`, `MainWindow`)
- **Functions/methods:** snake_case (`initUI`, `load_data`, `main`)
- **Variables:** snake_case (`csv_files`, `merged_df`)
- **Constants:** UPPER_SNAKE_CASE (`INPUT_PATH`, `OUTPUT_PATH`, `STARTTIME`)
- **Private methods:** prefix with underscore (`_private_method`)

### Types

Add type hints for function signatures and important variables. Use `pd.DataFrame` for pandas DataFrames:

```python
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    cctv_df: pd.DataFrame
```

### Error Handling

Use try/except for file I/O and data parsing. Catch specific exceptions:

```python
try:
    df = pd.read_csv(path)
except FileNotFoundError:
    print(f"File not found: {path}")
except pd.errors.EmptyDataError:
    print(f"Empty file: {path}")
```

### Data Processing

Use pandas for CSV operations. Use `ignore_index=True` when concatenating DataFrames. Set `index=False` when writing to CSV:

```python
merged_df = pd.concat(list_of_df, ignore_index=True)
merged_df.to_csv(output_path, index=False)
```

### PyQt6 Patterns

Inherit from QWidget/QMainWindow, use layouts (QVBoxLayout, QHBoxLayout, QGridLayout), initialize UI in separate `initUI()` method:

```python
class MapPage(QWidget):
    MAP_IMAGE_SIZE = int(885 / 3)
    sidebar_hidden = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

### Async/Await Patterns

Use asyncio for API calls:

```python
async def fetch_weather():
    async with NOAAClient(token=os.environ.get("NOAA_TOKEN")) as client:
        return await client.get_data(...)
```

### File Paths

Use relative paths from project root. Use `os.path.join()` or pathlib for path construction:

```python
INPUT_PATH = "../Data/Processed/data.csv"
OUTPUT_PATH = os.path.join("..", "Data", "Processed", "output.csv")
```

## Security Guidelines

### Never Commit Secrets

- Never commit API tokens, passwords, or secrets
- Use environment variables for sensitive data
- Create a `.env` file for local development (add to `.gitignore`)

### Using Environment Variables

```python
import os
from dotenv import load_dotenv

load_dotenv()
NOAA_TOKEN = os.environ.get("NOAA_TOKEN")
if not NOAA_TOKEN:
    raise ValueError("NOAA_TOKEN environment variable not set")
```

## Best Practices

1. Follow PEP 8 style guide
2. Single Responsibility: each script handles one task
3. Validate inputs before processing
4. Never commit sensitive data or credentials
5. Document required packages in README.md
6. Extract reusable logic into functions/classes
7. Define magic numbers as constants at module level

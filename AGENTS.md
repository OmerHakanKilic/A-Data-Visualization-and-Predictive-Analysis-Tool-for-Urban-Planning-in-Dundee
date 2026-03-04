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
│   ├── 06_tab_demo.py        # PyQt6 demo (tab navigation)
│   ├── 07_map_demo.py        # Main PyQt6 map visualization app
│   ├── 08_holidays.py        # Process UK holidays data
│   ├── 09_add_holiday_flag.py
│   ├── 10_fetch_weather_data.py  # Fetch weather from NOAA API
│   └── generate_map_images.py
├── Data/                    # Data directory
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

# Run PyQt6 applications
python 06_tab_demo.py
python 07_map_demo.py
```

### Dependencies

Install all: `pip install pandas PyQt6 noaa-cdo-api aiohttp python-dotenv`

### Running Tests

Currently no formal tests exist. If adding tests:

```bash
pytest tests/                    # Run all tests
pytest tests/test_file.py        # Run specific file
pytest tests/test_file.py::test_function_name  # Run single test
python -m unittest discover tests/
```

### Linting and Code Quality

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

### Imports

Standard library first, then third-party:

```python
import asyncio
import functools
import glob
import os
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from noaa_cdo_api import Extent, NOAAClient
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
```

- Use explicit imports (no `from module import *`), sort alphabetically within groups

### Naming Conventions

- **Classes:** PascalCase (`MainWindow`, `MapPage`)
- **Functions/methods:** snake_case (`initUI`, `load_data`)
- **Variables:** snake_case (`csv_files`, `merged_df`)
- **Constants:** UPPER_SNAKE_CASE (`STARTTIME`, `FINISHTIME`)
- **Private methods:** prefix with underscore (`_private_method`)

### Types

Add type hints for function signatures and important variables. Use `pd.DataFrame` for pandas DataFrames.

### Error Handling

Use try/except for operations that may fail (file I/O, data parsing). Catch specific exceptions when possible.

### Data Processing

Use pandas for CSV operations. Use `ignore_index=True` when concatenating DataFrames. Set `index=False` when writing to CSV.

### PyQt6 Patterns

Inherit from QWidget/QMainWindow, use layouts (QVBoxLayout, QHBoxLayout, QGridLayout), initialize UI in separate `initUI()` method.

```python
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

### Async/Await Patterns

Use asyncio for API calls and I/O operations:

```python
import asyncio
from noaa_cdo_api import NOAAClient

async def fetch_data():
    async with NOAAClient(token=os.environ.get("NOAA_TOKEN")) as client:
        return await client.get_data(...)

results = asyncio.run(fetch_data())
```

### File Paths

Use relative paths from project root or Code directory. Use `os.path.join()` for path construction.

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

### .env File Format

Create `Code/.env`: `NOAA_TOKEN=your_api_token_here`

### .gitignore Configuration

```
.env
.env.*
```

## Best Practices

1. Follow PEP 8 style guide
2. Single Responsibility: each script handles one task
3. Validate inputs before processing
4. Never commit sensitive data or credentials
5. Document required packages
6. Extract reusable logic into functions/classes
7. Define magic numbers as constants

# AGENTS.md - Big Data Project

Educational project for processing and visualizing CCTV data from Dundee, Scotland. Python scripts for data processing + PyQt6 GUI for map visualization.

## Project Structure

```
Code/                    # Python scripts and apps
  01-05_*.py            # Data processing pipeline
  08-12_*.py            # Weather & feature engineering
  13-16_*.py            # EDA, encoding, splitting
  06_tab_demo.py        # PyQt6 tab demo
  07_map_demo.py        # Basic map demo
  11_map_demo_refined.py # Map with histograms
Data/
  Raw/                  # Input data (CCTV, Holidays, Weather)
  Processed/            # Output data
Output/                 # Generated files
```

## Commands

### Run Data Pipeline (in order - scripts depend on previous outputs)
```bash
cd Code/ && for f in 01_*.py 02_*.py 03_*.py 04_*.py 05_*.py 08_*.py 09_*.py 10_*.py 12_*.py 13_*.py 14_*.py 15_*.py 16_*.py; do python "$f"; done
```

### Run GUI Apps
```bash
python Code/11_map_demo_refined.py   # Main map + histograms
python Code/07_map_demo.py          # Basic map
python Code/06_tab_demo.py           # Tab demo
```

### Lint & Format
```bash
pip install ruff black mypy
black Code/          # Format
ruff check Code/     # Lint
mypy Code/           # Type check
```

## Dependencies
```bash
pip install pandas matplotlib numpy PyQt6 noaa-cdo-api aiohttp python-dotenv
```

## Code Style

### Formatting
- Python 3.9+, f-strings, max line length: 100, 4-space indent
- Blank lines between top-level definitions, trailing commas for multi-line
- Always use `if __name__ == "__main__":` guard

### Imports (3 groups, alphabetical within each)
```python
import os
from datetime import datetime

import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow
```
- No `from module import *`
- Explicit imports only

### Naming
- Classes: `PascalCase` (MapPage, MainWindow)
- Functions/methods: `snake_case` (initUI, load_data)
- Variables: `snake_case` (csv_files, merged_df)
- Constants: `UPPER_SNAKE_CASE` (INPUT_PATH, STARTTIME)
- Private methods: prefix with `_` (_private_method)

### Types
Add type hints for function signatures:
```python
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    cctv_df: pd.DataFrame
```

### Error Handling
Catch specific exceptions:
```python
try:
    df = pd.read_csv(path)
except FileNotFoundError:
    print(f"File not found: {path}")
except pd.errors.EmptyDataError:
    print(f"Empty file: {path}")
```

### Data Processing
```python
merged_df = pd.concat(list_of_df, ignore_index=True)
merged_df.to_csv(output_path, index=False)
```

### PyQt6 Patterns
```python
class MapPage(QWidget):
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

### Async/Await
```python
async def fetch_weather():
    async with NOAAClient(token=os.environ.get("NOAA_TOKEN")) as client:
        return await client.get_data(...)
```

### File Paths
```python
INPUT_PATH = "../Data/Processed/data.csv"
OUTPUT_PATH = os.path.join("..", "Data", "Processed", "output.csv")
```

## Security

- Never commit API tokens, passwords, or secrets
- Use environment variables via `python-dotenv`
- Add `.env` to `.gitignore`

```python
import os
from dotenv import load_dotenv
load_dotenv()
NOAA_TOKEN = os.environ.get("NOAA_TOKEN")
if not NOAA_TOKEN:
    raise ValueError("NOAA_TOKEN environment variable not set")
```

## Best Practices

1. Follow PEP 8
2. Single Responsibility: each script handles one task
3. Validate inputs before processing
4. Extract reusable logic into functions/classes
5. Define magic numbers as constants at module level

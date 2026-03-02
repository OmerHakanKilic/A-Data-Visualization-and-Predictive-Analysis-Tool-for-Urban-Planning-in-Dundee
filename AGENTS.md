# AGENTS.md - Big Data Project Development Guide

This document provides guidance for agentic coding agents working in this repository.

## Project Overview

This is a Big Data educational project focused on processing and visualizing CCTV data from Dundee, Scotland. The codebase consists of Python scripts for data processing and a PyQt6-based GUI application for map visualization.

## Project Structure

```
Big Data/
├── Python Code/           # All Python scripts and applications
│   ├── 01_merge_csv_script.py
│   ├── 02_normalize_time_from_UTC.py
│   ├── 03_reformat_time.py
│   ├── 04_merge_duplicates.py
│   ├── 05_convert_floats_to_int.py
│   ├── 06_tab_demo.py     # PyQt6 demo (tab navigation)
│   ├── 07_map_demo.py     # Main PyQt6 map visualization app
│   └── generate_map_images.py
├── Data/                  # Data directory
│   ├── Raw/               # Raw input data (CSV files)
│   ├── Processed/         # Processed output data
│   └── MapImages/         # Map images for visualization
├── Output/                # Generated output files
└── Documents/             # Project documentation (sensitive)
```

## Build and Runtime Commands

### Running Python Scripts

Execute data processing scripts in order (they depend on previous outputs):

```bash
# Run individual scripts (from Python Code directory)
cd Python\ Code/
python 01_merge_csv_script.py
python 02_normalize_time_from_UTC.py
python 03_reformat_time.py
python 04_merge_duplicates.py
python 05_convert_floats_to_int.py

# Run PyQt6 applications
python 06_tab_demo.py
python 07_map_demo.py
```

### Dependencies

The project uses the following Python packages:
- `pandas` - Data processing and CSV manipulation
- `PyQt6` - GUI framework for map visualization

Install dependencies:
```bash
pip install pandas PyQt6
```

### Running a Single Test

**Note:** There are currently no formal tests in this project. If adding tests:

```bash
# With pytest (recommended)
pytest tests/                    # Run all tests
pytest tests/test_file.py        # Run specific test file
pytest tests/test_file.py::test_function_name  # Run single test

# With unittest
python -m unittest discover tests/
python -m unittest tests.test_module
```

### Linting and Code Quality

Install and run linters:

```bash
# Install development dependencies
pip install ruff black mypy

# Format code
black Python\ Code/

# Lint code
ruff check Python\ Code/

# Type checking (if type hints added)
mypy Python\ Code/
```

## Code Style Guidelines

### Python Version

- Target Python 3.9+ for compatibility
- Use f-strings for string formatting (not % formatting or .format())

### Imports

Standard library imports first, third-party imports second:

```python
import glob
import os

import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QWidget,
)
```

- Use explicit imports (avoid `from module import *`)
- Group related imports from same package
- Sort imports alphabetically within groups

### Naming Conventions

- **Classes:** PascalCase (`class MainWindow`, `class MapPage`)
- **Functions/methods:** snake_case (`def initUI`, `def loadData`)
- **Variables:** snake_case (`csv_files`, `merged_df`)
- **Constants:** UPPER_SNAKE_CASE (`STARTTIME`, `FINISHTIME`)
- **Private methods:** prefix with underscore (`def _private_method`)

### Types

- Add type hints for function signatures and important variables
- Use `pd.DataFrame` for pandas DataFrames
- Example from codebase:

```python
def apply_tint(self, pixmap: QPixmap, color: QColor) -> QPixmap:
    tinted = pixmap.copy()
    painter = QPainter(tinted)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
    painter.fillRect(tinted.rect(), color)
    painter.end()
    return tinted
```

### Formatting

- Maximum line length: 100 characters (or 88 for Black default)
- Use 4 spaces for indentation (not tabs)
- Add blank lines between top-level definitions
- Use parentheses for line continuation:

```python
scaledPixmap_308 = pixmap_308.scaled(
    MapPage.MAP_IMAGE_SIZE, MapPage.MAP_IMAGE_SIZE
)
```

- Use trailing commas for multi-line imports/collections:

```python
seasonDropMenu.addItems(
    [
        "Winter",
        "Spring",
        "Summer",
        "Autumn",
    ]
)
```

### Error Handling

- Use try/except blocks for operations that may fail (file I/O, data parsing)
- Catch specific exceptions when possible
- Log errors or provide meaningful error messages
- Example:

```python
try:
    merged_df.to_csv("../Data/Processed/01_Merged_CCTV_data.csv", index=False)
except IOError as e:
    print(f"Error saving file: {e}")
    raise
```

### Comments

- Avoid unnecessary comments; let code be self-documenting
- Use docstrings for classes and complex functions:

```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 1000, 1000)
        self.stack = QStackedWidget()
        self.initUI()
        self.loadData()
```

### Data Processing Conventions

- Use pandas for CSV operations
- Use `ignore_index=True` when concatenating DataFrames
- Set `index=False` when writing to CSV to avoid extra column
- Validate data after processing steps

### PyQt6 Patterns

- Follow the standard Qt widget pattern (inherit from QWidget/QMainWindow)
- Use layouts (QVBoxLayout, QHBoxLayout, QGridLayout) for UI structure
- Initialize UI in separate `initUI()` method
- Use `main()` function as entry point:

```python
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
```

### File Paths

- Use relative paths from project root or Python Code directory
- Use `os.path.join()` for path construction:

```python
csv_files = glob.glob(os.path.join(target_csv_folder, "*.csv"))
```

### Best Practices

1. **Idiomatic Python:** Follow PEP 8 style guide
2. **Single Responsibility:** Each script should handle one data processing task
3. **Data Validation:** Validate inputs before processing
4. **No Secrets:** Never commit sensitive data or credentials
5. **Dependencies:** Document required packages in code comments
6. **Modularity:** Extract reusable logic into functions/classes
7. **Constants:** Define magic numbers as class constants or module-level constants

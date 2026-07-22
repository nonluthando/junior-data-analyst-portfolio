# CSV Data Cleaning Tool

A configurable pandas command-line tool for preparing CSV data for analysis or machine-learning workflows.

## Features

- Standard and aggressive cleaning profiles
- Whitespace normalisation without converting missing values into strings
- Duplicate and fully empty row removal
- Median or zero imputation for numeric columns
- Mode or `N/A` imputation for text columns
- Human-readable cleaning audit log
- CSV output with optional Excel export

## Run

```bash
pip install pandas openpyxl
python csv_cleaning_tool.py
```

The tool asks for a CSV path, cleaning profile, and whether to produce an Excel copy.

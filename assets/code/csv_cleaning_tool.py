"""CSV Data Cleaning Tool.

Provides configurable cleaning profiles for preparing CSV datasets for
analysis and machine-learning workflows. The tool records every cleaning
operation and can export the cleaned data to CSV and Excel.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


CleaningProfile = dict[str, Any]


def show_profiles() -> None:
    print("Select a cleaning profile:")
    print(
        """
1. Standard (safe cleaning)
   - Trim whitespace in text columns
   - Drop duplicate rows
   - Fill missing numeric values with the median
   - Fill missing text values with the mode or 'N/A'

2. Aggressive (heavy cleaning)
   - Drop fully empty rows
   - Trim whitespace in text columns
   - Drop duplicate rows
   - Fill missing numeric values with 0
   - Fill missing text values with 'N/A'
"""
    )


def get_profile(choice: str) -> CleaningProfile | None:
    profiles: dict[str, CleaningProfile] = {
        "1": {
            "name": "Standard",
            "strip_whitespace": True,
            "drop_duplicates": True,
            "numeric_fill": "median",
            "text_fill": "mode",
            "drop_empty_rows": False,
        },
        "2": {
            "name": "Aggressive",
            "strip_whitespace": True,
            "drop_duplicates": True,
            "numeric_fill": "zero",
            "text_fill": "na",
            "drop_empty_rows": True,
        },
    }
    return profiles.get(choice)


def clean_data(
    dataframe: pd.DataFrame, profile: CleaningProfile
) -> tuple[pd.DataFrame, list[str], dict[str, int]]:
    """Return a cleaned copy of a DataFrame, an audit log, and row summary."""
    df = dataframe.copy()
    log: list[str] = []
    initial_rows = len(df)

    # Empty rows must be removed before filling missing values.
    if profile["drop_empty_rows"]:
        before = len(df)
        df = df.dropna(how="all")
        log.append(f"Dropped {before - len(df)} fully empty rows.")

    if profile["strip_whitespace"]:
        text_columns = df.select_dtypes(include=["object", "string"]).columns
        for column in text_columns:
            # Preserve missing values instead of converting NaN to the string 'nan'.
            df[column] = df[column].apply(
                lambda value: value.strip() if isinstance(value, str) else value
            )
        log.append("Trimmed whitespace in text columns.")

    if profile["drop_duplicates"]:
        before = len(df)
        df = df.drop_duplicates()
        log.append(f"Dropped {before - len(df)} duplicate rows.")

    for column in df.select_dtypes(include="number").columns:
        missing_count = int(df[column].isna().sum())
        if missing_count == 0:
            continue

        if profile["numeric_fill"] == "median":
            median = df[column].median()
            fill_value = 0 if pd.isna(median) else median
            df[column] = df[column].fillna(fill_value)
            log.append(
                f"Filled {missing_count} missing numeric values in '{column}' "
                f"with median ({fill_value})."
            )
        else:
            df[column] = df[column].fillna(0)
            log.append(
                f"Filled {missing_count} missing numeric values in '{column}' with 0."
            )

    text_columns = df.select_dtypes(include=["object", "string"]).columns
    for column in text_columns:
        missing_count = int(df[column].isna().sum())
        if missing_count == 0:
            continue

        if profile["text_fill"] == "mode":
            mode_values = df[column].mode(dropna=True)
            fill_value = mode_values.iloc[0] if not mode_values.empty else "N/A"
        else:
            fill_value = "N/A"

        df[column] = df[column].fillna(fill_value)
        log.append(
            f"Filled {missing_count} missing text values in '{column}' "
            f"with '{fill_value}'."
        )

    final_rows = len(df)
    summary = {
        "initial_rows": initial_rows,
        "final_rows": final_rows,
        "rows_removed": initial_rows - final_rows,
    }
    return df, log, summary


def export_cleaned_data(
    dataframe: pd.DataFrame, input_path: Path, export_excel: bool
) -> tuple[Path, Path | None]:
    output_csv = input_path.with_name(f"{input_path.stem}_cleaned.csv")
    dataframe.to_csv(output_csv, index=False)

    output_excel: Path | None = None
    if export_excel:
        output_excel = input_path.with_name(f"{input_path.stem}_cleaned.xlsx")
        dataframe.to_excel(output_excel, index=False)

    return output_csv, output_excel


def main() -> None:
    print("=== CSV Data Cleaning Tool ===")
    file_name = input("Please enter the CSV file name: ").strip()
    csv_path = Path(file_name)

    if not csv_path.exists():
        print("File not found.")
        return
    if csv_path.suffix.lower() != ".csv":
        print("Please provide a CSV file.")
        return

    try:
        df = pd.read_csv(csv_path)
    except (OSError, UnicodeDecodeError, pd.errors.ParserError) as error:
        print(f"Could not read the CSV file: {error}")
        return

    print("File loaded successfully.")
    print("Initial shape:", df.shape)

    show_profiles()
    profile = get_profile(input("Enter your choice (1 or 2): ").strip())
    if profile is None:
        print("Invalid profile selected.")
        return

    print(f"Applying {profile['name']} cleaning profile...")
    cleaned_df, log, summary = clean_data(df, profile)

    print(f"Initial number of rows: {summary['initial_rows']}")
    print(f"Final number of rows: {summary['final_rows']}")
    print(f"Number of rows removed: {summary['rows_removed']}")

    print("\n--- Cleaning Log ---")
    for entry in log:
        print("-", entry)

    export_excel = input("Also export an Excel file? (y/n): ").strip().lower() == "y"
    output_csv, output_excel = export_cleaned_data(
        cleaned_df, csv_path, export_excel
    )

    print(f"\nCleaned CSV saved as: {output_csv}")
    if output_excel is not None:
        print(f"Excel file created: {output_excel}")

    print("\n--- Sample of Cleaned Data ---")
    print(cleaned_df.head())


if __name__ == "__main__":
    main()

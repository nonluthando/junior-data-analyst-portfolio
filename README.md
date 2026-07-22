# Luthando Mbuyane — Data Analyst Portfolio v4

A responsive, dependency-free static portfolio designed for GitHub Pages.

## What changed in v4

- Added the technical notebook behind the e-commerce funnel case study.
- Added cleanly renamed copies of the sales SQL pipeline and video-game sales analysis.
- Removed duplicate and `Untitled` notebook files.
- Added a supporting-notebooks section with direct downloads.
- Removed stale Colab upload-widget output while retaining useful analysis outputs.

## Files

- `index.html` — page content
- `styles.css` — full responsive styling
- `script.js` — mobile navigation, sticky header and reveal effects
- `assets/reports/` — downloadable PDF case studies
- `assets/code/` — configurable CSV cleaning tool, requirements and project notes
- `assets/notebooks/` — three cleanly named supporting Jupyter notebooks
- `assets/images/` — project visuals and favicon

## Supporting notebooks

- `ecommerce-funnel-analysis.ipynb` — funnel reconstruction, drop-off analysis and behavioural segmentation.
- `sales-data-analysis-sql-pipeline.ipynb` — pandas, SQLite, SQL aggregation, exports and sales trend visualisation.
- `video-game-sales-analysis.ipynb` — additional DuckDB/SQL exploration of regional video-game sales.

The notebooks were originally developed in Google Colab. Upload and download cells may require Colab or small path changes when run locally.

## Preview locally

Open `index.html` directly in a browser, or run a local server:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Publish on GitHub Pages

1. Upload all files and folders to the root of the portfolio repository.
2. In GitHub, open **Settings → Pages**.
3. Set the source to **Deploy from a branch**.
4. Choose the `main` branch and `/ (root)` folder.
5. Save.

## Data cleaning tool

The portfolio includes a corrected and consolidated version of the CSV cleaning pipeline. It preserves missing text values during whitespace trimming, removes fully empty rows before imputation and optionally exports an Excel copy.

Run it with:

```bash
pip install -r assets/code/requirements.txt
python assets/code/csv_cleaning_tool.py
```

## Before publishing

- Add a CV download only when the latest CV is ready.
- Add LinkedIn when the preferred public profile URL is confirmed.

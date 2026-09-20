# Ford GoBike Project

This project separates the reusable Python logic from the original EDA notebook.

## Structure

- `config.py` - project configuration and column lists.
- `src/data_loading.py` - loading and dataset overview.
- `src/preprocessing.py` - cleaning and validation functions.
- `src/feature_engineering.py` - age and trip-duration features.
- `src/analysis.py` - reusable analysis calculations.
- `run_pipeline.py` - runs the reusable preprocessing pipeline.

## Important note

The current source data contains `start_time` and `end_time` values in `MM:SS.f` format, so they are not parsed directly as normal timestamps.

The notebook's real date information is therefore not sufficient to reliably create weekday/month/weekend features. A real date column is required for those dashboard features.

## Run

Place the CSV file here:

`data/fordgobike-tripdataFor201902.csv`

Then run:

```bash
python run_pipeline.py
```

The pipeline writes:

`data/fordgobike_cleaned.csv`


## Dash Dashboard

The dashboard uses Plotly Express for chart creation and Dash callbacks for
interactive filtering.

### Dashboard structure

- Overview KPIs
- Time Analysis
- User Analysis
- Station / Trip Analysis
- Relationship Analysis

### Run

From the project root:

```bash
pip install -r requirements.txt
python dashboard/app.py
```

Then open the local Dash address shown in the terminal.

The app first looks for:

`data/fordgobike_cleaned.csv`

and falls back to:

`data/fordgobike-tripdataFor201902.csv`

if the cleaned file has not been generated yet.

### Important source-data limitation

The supplied `start_time` and `end_time` fields are stored as `MM:SS.f`
values rather than full calendar timestamps. Because of that, the dashboard
does not invent weekday/month/date information. The time section works with
the time representation actually available in the source.

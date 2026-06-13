# test

A Streamlit dashboard for checking DFW permit / certificate-of-occupancy exports and scoring likely sign-company leads.

## What it does

- One-click buttons for Dallas, Fort Worth, Plano, Frisco, McKinney, Arlington
- Filters for restaurant, retail, medical, tenant finish-out, commercial remodel, CO, and sign-related work
- Scores each lead from 0-100
- Lets you download filtered leads as CSV
- Supports manual CSV/XLSX exports from city portals immediately
- Supports direct CSV/API URLs once you add them in `sources.py`

## Install

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit gives you, usually `http://localhost:8501`.

## How to add city exports

1. Go to the city portal from the dashboard.
2. Export recent issued permits / COs as CSV or XLSX.
3. Put the file in:

```text
data/manual_uploads/
```

4. Include the city name in the file name, for example:

```text
data/manual_uploads/frisco_permits_june.csv
data/manual_uploads/arlington_issued_permits.csv
```

5. Click the city button in the app.

## How to add automatic data URLs

Edit `sources.py` and add CSV/API export URLs under that city's `csv_urls` list.

Example:

```python
"Arlington": {
    "portal": "https://opendata.arlingtontx.gov/datasets/issued-permits",
    "notes": "...",
    "csv_urls": ["PASTE_CSV_EXPORT_URL_HERE"],
}
```

## Good lead keywords

Restaurant, coffee, retail, tenant finish-out, tenant improvement, medical, urgent care, commercial remodel, salon, fitness, certificate of occupancy, sign, channel letters, monument, storefront.

## Notes

Some cities use public portals without stable CSV APIs. This app is built to work immediately with manual exports, and to become fully automatic when stable export/API URLs are added.

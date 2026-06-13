from __future__ import annotations

from pathlib import Path
from typing import Iterable
import io
import pandas as pd
import requests

from lead_scoring import is_target_lead, score_lead, category
from sources import CITY_SOURCES

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
MANUAL_DIR = DATA_DIR / "manual_uploads"
MANUAL_DIR.mkdir(parents=True, exist_ok=True)

STANDARD_COLUMNS = [
    "city", "permit_number", "project_name", "address", "permit_type", "description",
    "issue_date", "estimated_value", "contractor", "owner", "category", "score", "source_url"
]

POSSIBLE_COLUMN_MAP = {
    "permit_number": ["permit_number", "permitnumber", "permit_no", "permit no", "permit", "record_id", "permitid", "record number"],
    "project_name": ["project_name", "project name", "business_name", "business name", "name", "tenant", "foldername", "record name"],
    "address": ["address", "full_address", "full address", "site address", "location", "property address", "street address"],
    "permit_type": ["permit_type", "permit type", "type", "record type", "work class", "permitclass", "permit class"],
    "description": ["description", "work_description", "work description", "scope", "project description", "comments", "workclass", "permitdescription"],
    "issue_date": ["issue_date", "issue date", "issued", "issued date", "date issued", "permit issued date"],
    "estimated_value": ["estimated_value", "valuation", "declared valuation", "job value", "project value", "value"],
    "contractor": ["contractor", "contractor name", "applicant", "applicant name", "general contractor"],
    "owner": ["owner", "owner name", "property owner"],
}


def _clean_col(name: str) -> str:
    return str(name).strip().lower().replace("_", " ")


def _pick_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    cleaned = {_clean_col(c): c for c in df.columns}
    for candidate in candidates:
        if candidate in cleaned:
            return cleaned[candidate]
    for candidate in candidates:
        for clean, original in cleaned.items():
            if candidate in clean:
                return original
    return None


def read_url_csv(url: str) -> pd.DataFrame:
    response = requests.get(url, timeout=30, headers={"User-Agent": "DFWSignLeadDashboard/1.0"})
    response.raise_for_status()
    return pd.read_csv(io.StringIO(response.text))


def read_manual_files(city: str) -> list[pd.DataFrame]:
    frames: list[pd.DataFrame] = []
    for path in MANUAL_DIR.glob("*"):
        if city.lower().replace(" ", "") not in path.stem.lower().replace(" ", ""):
            continue
        try:
            if path.suffix.lower() == ".csv":
                frames.append(pd.read_csv(path))
            elif path.suffix.lower() in {".xlsx", ".xls"}:
                frames.append(pd.read_excel(path))
        except Exception:
            continue
    return frames


def normalize(city: str, df: pd.DataFrame, source_url: str = "manual/upload") -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=STANDARD_COLUMNS)

    out = pd.DataFrame()
    out["city"] = city
    for target, candidates in POSSIBLE_COLUMN_MAP.items():
        col = _pick_column(df, candidates)
        out[target] = df[col] if col else ""

    combined = (
        out["project_name"].astype(str) + " " + out["address"].astype(str) + " " +
        out["permit_type"].astype(str) + " " + out["description"].astype(str) + " " +
        out["contractor"].astype(str) + " " + out["owner"].astype(str)
    )
    out["category"] = combined.apply(category)
    out["score"] = combined.apply(score_lead)
    out["source_url"] = source_url
    out = out[combined.apply(is_target_lead)].copy()
    out = out.sort_values(["score", "issue_date"], ascending=[False, False], na_position="last")
    return out[STANDARD_COLUMNS]


def fetch_city(city: str) -> pd.DataFrame:
    cfg = CITY_SOURCES[city]
    frames: list[pd.DataFrame] = []
    for url in cfg.get("csv_urls", []):
        try:
            frames.append(normalize(city, read_url_csv(url), url))
        except Exception as exc:
            frames.append(pd.DataFrame([{
                "city": city, "permit_number": "", "project_name": "SOURCE ERROR", "address": "",
                "permit_type": "", "description": f"Could not download {url}: {exc}", "issue_date": "",
                "estimated_value": "", "contractor": "", "owner": "", "category": "Setup Needed",
                "score": 0, "source_url": cfg.get("portal", "")
            }]))
    for manual in read_manual_files(city):
        frames.append(normalize(city, manual, "manual upload"))
    if not frames:
        return pd.DataFrame([{
            "city": city, "permit_number": "", "project_name": "Add data source or upload export", "address": "",
            "permit_type": "", "description": cfg.get("notes", ""), "issue_date": "",
            "estimated_value": "", "contractor": "", "owner": "", "category": "Setup Needed",
            "score": 0, "source_url": cfg.get("portal", "")
        }])[STANDARD_COLUMNS]
    return pd.concat(frames, ignore_index=True)[STANDARD_COLUMNS]

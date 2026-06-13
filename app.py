from __future__ import annotations

from pathlib import Path
from datetime import datetime
import pandas as pd
import streamlit as st

from permit_scrapers.dallas import get_dallas
from permit_scrapers.fortworth import get_fortworth
from permit_scrapers.plano import get_plano
from permit_scrapers.frisco import get_frisco
from permit_scrapers.mckinney import get_mckinney
from permit_scrapers.arlington import get_arlington
from sources import CITY_SOURCES

st.set_page_config(page_title="DFW Sign Lead Finder", layout="wide")

CITY_FUNCS = {
    "Dallas": get_dallas,
    "Fort Worth": get_fortworth,
    "Plano": get_plano,
    "Frisco": get_frisco,
    "McKinney": get_mckinney,
    "Arlington": get_arlington,
}

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)

st.title("DFW Sign Lead Finder")
st.caption("One-click permit and CO lead dashboard for sign sales teams.")

with st.sidebar:
    st.header("Filters")
    min_score = st.slider("Minimum lead score", 0, 100, 70)
    show_setup = st.checkbox("Show setup-needed rows", True)
    st.header("Manual Uploads")
    st.write("Save city exports into `data/manual_uploads/` with the city name in the file, like `frisco_permits.csv`.")


def filter_df(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    filtered = df.copy()
    if not show_setup:
        filtered = filtered[filtered["category"] != "Setup Needed"]
    return filtered[filtered["score"].fillna(0).astype(int) >= min_score]


def display_results(city: str, df: pd.DataFrame) -> None:
    cfg = CITY_SOURCES.get(city, {})
    st.subheader(city)
    if cfg.get("portal"):
        st.markdown(f"[Open {city} permit portal]({cfg['portal']})")
    df = filter_df(df)
    if df.empty:
        st.info("No matching leads found for the current filters.")
        return
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "source_url": st.column_config.LinkColumn("Source"),
            "score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100),
        },
    )
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(f"Download {city} CSV", csv, f"{city.lower().replace(' ', '_')}_sign_leads.csv", "text/csv")

st.header("Check a city")
cols = st.columns(3)
for idx, city in enumerate(CITY_FUNCS):
    with cols[idx % 3]:
        if st.button(city, use_container_width=True):
            st.session_state["selected_city"] = city

if st.button("All Cities", type="primary", use_container_width=True):
    st.session_state["selected_city"] = "All Cities"

selected = st.session_state.get("selected_city", "All Cities")

if selected == "All Cities":
    frames = [func() for func in CITY_FUNCS.values()]
    all_df = pd.concat(frames, ignore_index=True)
    display_results("All Cities", all_df)
else:
    display_results(selected, CITY_FUNCS[selected]())

st.divider()
st.header("City source status")
status = pd.DataFrame([
    {"City": c, "Portal": cfg.get("portal"), "Configured CSV/API URLs": len(cfg.get("csv_urls", [])), "Notes": cfg.get("notes", "")}
    for c, cfg in CITY_SOURCES.items()
])
st.dataframe(status, use_container_width=True, hide_index=True, column_config={"Portal": st.column_config.LinkColumn("Portal")})

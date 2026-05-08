import os
import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="Grateful Dead Ultimate Fan App",
    layout="wide"
)

st.title("Grateful Dead Ultimate Fan App")

CACHE_FILE = "cached_setlists.csv"


@st.cache_data(show_spinner=True)
def load_full_setlists():

    # -----------------------
    # USE CACHE IF EXISTS
    # -----------------------

    if os.path.exists(CACHE_FILE):
        st.info("Loading cached dataset...")
        return pd.read_csv(CACHE_FILE)

    st.info("Fetching data from Bearly Dead API...")

    base_url = "https://bearlydead.songfishapp.com/api/v2/"

    # -----------------------
    # LOAD SHOWS
    # -----------------------

    shows = []
    page = 1

    while True:

        resp = requests.get(f"{base_url}shows.json?page={page}")

        if resp.status_code != 200:
            st.error(f"Failed loading shows page {page}")
            break

        data = resp.json().get("data", [])

        if not data:
            break

        shows.extend(data)

        page += 1

    df_shows = pd.DataFrame(shows)

    # -----------------------
    # LOAD SETLISTS
    # -----------------------

    setlists = []
    page = 1

    while True:

        resp = requests.get(f"{base_url}setlists.json?page={page}")

        if resp.status_code != 200:
            st.error(f"Failed loading setlists page {page}")
            break

        data = resp.json().get("data", [])

        if not data:
            break

        setlists.extend(data)

        page += 1

    df_sets = pd.DataFrame(setlists)

    # -----------------------
    # MERGE
    # -----------------------

    df = df_sets.merge(
        df_shows,
        on="show_id",
        how="left",
        suffixes=("_set", "_show")
    )

    # -----------------------
    # CLEANING
    # -----------------------

    if "showdate" in df.columns:
        df["showdate"] = pd.to_datetime(
            df["showdate"],
            errors="coerce"
        )

    string_cols = [
        "songname",
        "venuename",
        "city",
        "state",
        "country",
        "tourname"
    ]

    for col in string_cols:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.title()
            )

    # -----------------------
    # SAVE CACHE
    # -----------------------

    df.to_csv(CACHE_FILE, index=False)

    return df


# -----------------------
# LOAD DATA
# -----------------------

df = load_full_setlists()

# -----------------------
# DISPLAY
# -----------------------

st.success(f"Loaded {len(df):,} rows")

st.dataframe(
    df[
        [
            "showdate",
            "songname",
            "venuename",
            "city",
            "state"
        ]
    ].head(50)
)
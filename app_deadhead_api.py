import os
import pandas as pd
import requests
import streamlit as st

# -----------------------------------
# PAGE SETUP
# -----------------------------------

st.set_page_config(
    page_title="Grateful Dead Ultimate Fan App",
    layout="wide"
)

st.title("Grateful Dead Ultimate Fan App")

CACHE_FILE = "cached_setlists.csv"


# -----------------------------------
# LOAD DATA
# -----------------------------------

@st.cache_data(show_spinner=True)
def load_full_setlists():

    # -------------------------------
    # USE CACHE IF AVAILABLE
    # -------------------------------

    if os.path.exists(CACHE_FILE):

        st.info("Loading cached dataset...")

        df = pd.read_csv(CACHE_FILE)

        return df

    # -------------------------------
    # API BASE
    # -------------------------------

    st.info("Fetching data from Bearly Dead API...")

    base_url = "https://bearlydead.songfishapp.com/api/v2/"

    # -------------------------------
    # LOAD SHOWS (ONLY PAGE 1)
    # -------------------------------

    resp_shows = requests.get(
        f"{base_url}shows.json?page=1"
    )

    st.write("SHOWS STATUS:", resp_shows.status_code)

    shows_data = resp_shows.json()

    shows = shows_data.get("data", [])

    df_shows = pd.DataFrame(shows)

    st.write(
        "SHOWS ROWS:",
        len(df_shows)
    )

    # -------------------------------
    # LOAD SETLISTS (ONLY PAGE 1)
    # -------------------------------

    resp_sets = requests.get(
        f"{base_url}setlists.json?page=1"
    )

    st.write("SETLIST STATUS:", resp_sets.status_code)

    setlists_data = resp_sets.json()

    setlists = setlists_data.get("data", [])

    df_sets = pd.DataFrame(setlists)

    st.write(
        "SETLIST ROWS:",
        len(df_sets)
    )

    # -------------------------------
    # MERGE
    # -------------------------------

    df = df_sets.merge(
        df_shows,
        on="show_id",
        how="left",
        suffixes=("_set", "_show")
    )

    # -------------------------------
    # CLEAN DATA
    # -------------------------------

    if "showdate_set" in df.columns:

        df["showdate_set"] = pd.to_datetime(
            df["showdate_set"],
            errors="coerce"
        )

    text_columns = [
        "songname",
        "venuename_set",
        "city_set",
        "state_set",
        "country_set",
        "tourname_set"
    ]

    for col in text_columns:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.title()
            )

    # -------------------------------
    # SAVE CACHE
    # -------------------------------

    df.to_csv(
        CACHE_FILE,
        index=False
    )

    return df


# -----------------------------------
# RUN LOADER
# -----------------------------------

df = load_full_setlists()

# -----------------------------------
# DISPLAY RESULTS
# -----------------------------------

st.success(
    f"Loaded {len(df):,} setlist rows"
)

display_cols = [
    "showdate_set",
    "songname",
    "venuename_set",
    "city_set",
    "state_set"
]

existing_cols = [
    col for col in display_cols
    if col in df.columns
]

st.dataframe(
    df[existing_cols].head(50)
)
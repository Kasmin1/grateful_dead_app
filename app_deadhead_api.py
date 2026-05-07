import os
import pandas as pd
import numpy as np
import requests
import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
import time

st.set_page_config(page_title="Grateful Dead Ultimate Fan App", layout="wide")
st.title("?? Grateful Dead Ultimate Fan App — API + Cache")

CACHE_FILE = "cached_setlists.csv"

@st.cache_data(show_spinner=True)
def load_full_setlists():

    if os.path.exists(CACHE_FILE):
        st.info("Loading dataset from local cache...")
        return pd.read_csv(CACHE_FILE)

    st.info("Fetching dataset from Bearly Dead API...")
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

    st.write("SHOWS COLUMNS:", df_shows.columns.tolist())

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

    st.write("SETLIST COLUMNS:", df_sets.columns.tolist())

   # -----------------------
# DEBUG COLUMN NAMES
# -----------------------

st.write("SHOWS COLUMNS:", df_shows.columns.tolist())
st.write("SETLIST COLUMNS:", df_sets.columns.tolist())

# -----------------------
# DETERMINE MERGE KEY
# -----------------------

possible_show_cols = ["show_id", "id", "showid"]

show_col_shows = None
show_col_sets = None

for col in possible_show_cols:
    if col in df_shows.columns:
        show_col_shows = col

for col in possible_show_cols:
    if col in df_sets.columns:
        show_col_sets = col

st.write("SHOW MERGE COL:", show_col_shows)
st.write("SETLIST MERGE COL:", show_col_sets)

if show_col_shows is None or show_col_sets is None:
    st.error("Could not determine merge columns")
    st.stop()

# -----------------------
# MERGE
# -----------------------

df = df_sets.merge(
    df_shows,
    left_on=show_col_sets,
    right_on=show_col_shows,
    how="left"
)

    # -----------------------
    # SAFE CLEANING
    # -----------------------
    for col in ["song", "venue", "city"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.title()

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df.to_csv(CACHE_FILE, index=False)

    return df

df = load_full_setlists()

st.write(df.head())                                                                                                                                                                     
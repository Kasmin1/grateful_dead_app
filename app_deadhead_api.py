import os
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Grateful Dead Ultimate Fan App", layout="wide")

st.title("Grateful Dead Ultimate Fan App")

CACHE_FILE = "cached_setlists.csv"


@st.cache_data(show_spinner=True)
def load_full_setlists():

    st.write("Starting API load...")

    base_url = "https://bearlydead.songfishapp.com/api/v2/"

    # -----------------------
    # LOAD SHOWS
    # -----------------------

    shows = []

    try:
        resp = requests.get(f"{base_url}shows.json?page=1")
        st.write("SHOWS STATUS:", resp.status_code)

        data = resp.json()

        st.write("SHOWS RAW:", data)

        shows = data.get("data", [])

    except Exception as e:
        st.error(f"SHOWS ERROR: {e}")
        st.stop()

    df_shows = pd.DataFrame(shows)

    st.write("SHOWS DF COLUMNS:", df_shows.columns.tolist())

    # -----------------------
    # LOAD SETLISTS
    # -----------------------

    setlists = []

    try:
        resp = requests.get(f"{base_url}setlists.json?page=1")
        st.write("SETLIST STATUS:", resp.status_code)

        data = resp.json()

        st.write("SETLIST RAW:", data)

        setlists = data.get("data", [])

    except Exception as e:
        st.error(f"SETLIST ERROR: {e}")
        st.stop()

    df_sets = pd.DataFrame(setlists)

    st.write("SETLIST DF COLUMNS:", df_sets.columns.tolist())

    # -----------------------
    # STOP BEFORE MERGE
    # -----------------------

    st.stop()


df = load_full_setlists()                                                                                 
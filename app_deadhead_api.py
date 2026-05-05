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
        df = pd.read_csv(CACHE_FILE, parse_dates=['date'])
        return df

    st.info("Fetching dataset from Bearly Dead API...")
    base_url = "https://bearlydead.songfishapp.com/api/v2/"
    
    shows = []
    page = 1
    while True:
        resp = requests.get(f"{base_url}shows.json?page={page}")
        data = resp.json().get("data", [])
        if not data:
            break
        shows.extend(data)
        page += 1

    df_shows = pd.DataFrame(shows)
    st.write("SHOWS COLUMNS:", df_shows.columns)

    setlists = []
    page = 1
    while True:
        resp = requests.get(f"{base_url}setlists.json?page={page}")
        data = resp.json().get("data", [])
        if not data:
            break
        setlists.extend(data)
        page += 1

    df_sets = pd.DataFrame(setlists)

    df = df_sets.merge(df_shows, left_on="show_id", right_on="id", how="left")

    df["date"] = pd.to_datetime(df["date"])
    df["song"] = df["song"].str.title()
    df["venue"] = df["venue"].str.title()
    df["city"] = df["city"].str.title()

    df.to_csv(CACHE_FILE, index=False)
    return df

df = load_full_setlists()

st.write(df.head())                                                                                                                                                                     
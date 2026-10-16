from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).parent / "data"

@st.cache_data
def get_player_stats():
    return pd.read_csv(DATA_DIR / "players.csv")

@st.cache_data
def get_team_stats():
    return pd.read_csv(DATA_DIR / "teams.csv")

def last_updated():
    return (DATA_DIR / "last_updated.txt").read_text().strip()
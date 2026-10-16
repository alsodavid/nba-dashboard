import streamlit as st
import pandas as pd
from data import get_player_stats, last_updated
import plotly.graph_objects as go

st.set_page_config(page_title="Player Comparison", page_icon="🏀", layout="wide")

st.title("Player Comparison")

with st.spinner("Loading player data..."):
    df = get_player_stats

player_names = sorted(df["PLAYER_NAME"].tolist())

col1, col2 = st.columns(2)
with col1:
    player1 = st.selectbox("Select Player 1:", player_names)
with col2:
    player2 = st.selectbox("Select Player 2:", player_names, index=1)

stats_to_compare = ["PTS", "AST", "REB", "STL", "BLK", "FG_PCT"]
stat_labels = ["Points", "Assists", "Rebounds", "Steals", "Blocks", "FG%"]

p1_data = df[df["PLAYER_NAME"] == player1].iloc[0]
p2_data = df[df["PLAYER_NAME"] == player2].iloc[0]

def normalize(value, col):
    col_max = df[col].max()
    col_min = df[col].min()
    if col_max == col_min:
        return 0
    return (value - col_min) / (col_max - col_min)

p1_normalized = [normalize(p1_data[stat], stat) for stat in stats_to_compare]
p2_normalized = [normalize(p2_data[stat], stat) for stat in stats_to_compare]

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=p1_normalized + [p1_normalized[0]],
    theta=stat_labels + [stat_labels[0]],
    fill="toself",
    name=player1,
    line_color="orange"
))
fig.add_trace(go.Scatterpolar(
    r=p2_normalized + [p2_normalized[0]],
    theta=stat_labels + [stat_labels[0]],
    fill="toself",
    name=player2,
    line_color="dodgerblue"
))
fig.update_layout(
    polar=dict(
        bgcolor="rgba(0,0,0,0)",
        radialaxis=dict(visible=False)
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)
left, right = st.columns([3, 2])

with left:
    st.plotly_chart(fig, use_container_width=True)

with right:
    p1_col, p2_col = st.columns(2)

    with p1_col:
        st.markdown(f"**{player1}**")
        for stat, label in zip(stats_to_compare, stat_labels):
            val = p1_data[stat]
            st.metric(label, f"{val:.1%}" if stat == "FG_PCT" else f"{val:.1f}")

    with p2_col:
        st.markdown(f"**{player2}**")
        for stat, label in zip(stats_to_compare, stat_labels):
            val = p2_data[stat]
            st.metric(label, f"{val:.1%}" if stat == "FG_PCT" else f"{val:.1f}")
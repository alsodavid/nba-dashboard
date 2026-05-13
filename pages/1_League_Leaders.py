import streamlit as st
import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats
import plotly.express as px

st.set_page_config(page_title="League Leaders", page_icon="🏀", layout="wide")

st.title("🏆 League Leaders")

stat_options = {
    "Points": "PTS",
    "Assists": "AST",
    "Rebounds": "REB",
    "Steals": "STL",
    "Blocks": "BLK"
}

selected_stat_label = st.selectbox("Select a stat category:", list(stat_options.keys()))
selected_stat = stat_options[selected_stat_label]

@st.cache_data(ttl=3600)
def get_leaders():
    stats = leaguedashplayerstats.LeagueDashPlayerStats(per_mode_detailed="PerGame")
    df = stats.get_data_frames()[0]
    return df

with st.spinner("Loading data..."):
    df = get_leaders()

df = df.sort_values(by=selected_stat, ascending=False).reset_index(drop=True)
df.insert(0, "RANK", df.index + 1)

display_cols = ["RANK", "PLAYER_NAME", "TEAM_ABBREVIATION", "GP", "MIN", selected_stat]
df_display = df[display_cols].head(20)
df_display.columns = ["Rank", "Player", "Team", "GP", "MIN", selected_stat_label]

st.subheader(f"Top 20 - {selected_stat_label} Per Game")
st.dataframe(df_display, use_container_width=True, hide_index=True)

st.subheader(f"Top 10 {selected_stat_label} Leaders")
top10 = df.head(10)
fig = px.bar(
    top10,
    x="PLAYER_NAME",
    y=selected_stat,
    color=selected_stat,
    color_continuous_scale="oranges",
    labels={"PLAYER_NAME": "Player", selected_stat: selected_stat_label}
)
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)
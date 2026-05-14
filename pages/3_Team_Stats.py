import streamlit as st
import pandas as pd
from nba_api.stats.endpoints import leaguedashteamstats
import plotly.express as px

st.set_page_config(page_title="Team Stats", page_icon="🏀", layout="wide")

st.title("Team Stats")

@st.cache_data(ttl=3600)
def get_team_stats():
    stats = leaguedashteamstats.LeagueDashTeamStats(per_mode_detailed="PerGame")
    df = stats.get_data_frames()[0]
    return df
with st.spinner("Loading team data..."):
    df=get_team_stats()

stat_options = {
    "Points": "PTS",
    "Assists": "AST",
    "Rebounds": "REB",
    "Steals": "STL",
    "Blocks": "BLK",
    "Field Goal %": "FG_PCT",
    "3-Point %": "FG3_PCT",
    "Turnovers": "TOV"
}

selected_stat_label = st.selectbox("Sort teams by:", list(stat_options.keys()))
selected_stat = stat_options[selected_stat_label]

ascending = selected_stat == "TOV"
df = df.sort_values(by=selected_stat, ascending=ascending).reset_index(drop=True)
df.insert(0, "RANK", df.index + 1)

display_cols = ["RANK", "TEAM_NAME", "GP", selected_stat]
df_display = df[display_cols].head(30)
df_display.columns = ["Rank", "Team", "GP", selected_stat_label]

st.subheader(f"All 30 Teams — {selected_stat_label} Per Game")
st.dataframe(df_display, use_container_width=True, hide_index=True)

fig = px.bar(
    df,
    x="TEAM_NAME",
    y=selected_stat,
    color=selected_stat,
    color_continuous_scale="oranges",
    labels={"TEAM_NAME": "Team", selected_stat: selected_stat_label}
)
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    xaxis_tickangle=-45,
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)
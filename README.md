# NBA Stats Dashboard

Interactive NBA statistics dashboard built with Python and Streamlit. 
Features league leaders, player comparison tools, and team analytics. 
Data sourced from the NBA API.

## Live Demo
[View the dashboard](https://davidalso-nba-dashboard.streamlit.app)

## Features
- **League Leaders** — Browse top players by points, assists, rebounds, steals, and blocks per game
- **Player Comparison** — Compare any two players head-to-head with a radar chart and stats breakdown
- **Team Stats** — View all 30 teams ranked by any stat category

## Tech Stack
- Python
- Streamlit
- Plotly
- pandas
- nba_api

## Run Locally
```bash
git clone https://github.com/alsodavid/nba-dashboard.git
cd nba-dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
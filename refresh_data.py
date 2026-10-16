from datetime import date
from pathlib import Path

from nba_api.stats.endpoints import leaguedashplayerstats, leaguedashteamstats

SEASON = "2025-26"
out = Path("data")
out.mkdir(exist_ok=True)

players = leaguedashplayerstats.LeagueDashPlayerStats(
    season=SEASON, per_mode_detailed="PerGame", timeout=60
).get_data_frames()[0]

teams = leaguedashteamstats.LeagueDashTeamStats(
    season=SEASON, per_mode_detailed="PerGame", timeout=60
).get_data_frames()[0]

players.to_csv(out / "players.csv", index=False)
teams.to_csv(out / "teams.csv", index=False)
(out / "last_updated.txt").write_text(date.today().isoformat())

print(f"Saved {len(players)} players and {len(teams)} teams for {SEASON}")
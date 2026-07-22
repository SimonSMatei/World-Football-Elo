import sqlite3
import pandas as pd
from pathlib import Path

PARENT_PATH = Path(__file__).parent.parent

DATA_PATH = PARENT_PATH / "databases"

def load_data() -> pd.DataFrame:
    results = pd.read_csv(DATA_PATH / "results.csv")
    results = results[results["date"] >= "2000-01-01"]

    shootouts = pd.read_csv(DATA_PATH / "shootouts.csv")
    shootouts = shootouts[shootouts["date"] >= "2000-01-01"]

    results = pd.merge(results, shootouts, on=["home_team", "away_team", "date"], how="left")

    results = results.dropna(subset=['home_score', 'away_score'])

    results['home_score'] = results['home_score'].astype(int)
    results['away_score'] = results['away_score'].astype(int)
    
    return results

def get_winner(row: pd.Series) -> str | None:
    
    if row["home_score"] > row["away_score"]:

        return row["home_team"]

    elif row["away_score"] > row["home_score"]:

        return row["away_team"]

    elif pd.notna(row["winner"]):

        return row["winner"]

    else:
        return None

def get_goal_diff(row: pd.Series) -> int:

    if pd.isna(row["match_winner"]):

        return 0

    elif row["match_winner"] == row["home_team"]:

        return row["home_score"] - row["away_score"]

    elif row["match_winner"] == row["away_team"]:

        return row["away_score"] - row["home_score"]

def remove_tournaments(file_name: str, results: pd.DataFrame) -> pd.DataFrame:
    file = PARENT_PATH / 'Scripts' / file_name

    tournaments = []

    with open(file) as f:
        for line in f:
            tournaments.append(line.strip('\n'))

    results = results[~results["tournament"].isin(tournaments)]

    return results

def remove_teams(file_name: str, results: pd.DataFrame) -> pd.DataFrame:
    file = PARENT_PATH / "Scripts" / file_name

    teams = []

    with open(file, encoding = "utf=8") as f:
        for line in f:
            teams.append(line.strip('\n'))
    
    results = results[results['home_team'].isin(teams) & results['away_team'].isin(teams)]

    return results


def build_database(results: pd.DataFrame) -> None:
    conn = sqlite3.connect(PARENT_PATH / "src" / "world_football_elo" / "data" / "international_football_data.db")
    cursor = conn.cursor()

    results.to_sql("matches", conn, if_exists="replace", index=False)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teams(
            team_name TEXT PRIMARY KEY,
            matches_played INTEGER,
            matches_won INTEGER,
            matches_lost INTEGER,
            matches_tied INTEGER,
            current_elo INTEGER,
            form REAL,
            is_provisional BOOLEAN,
            provisional_avg_elo REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS snapshots(
            date TEXT,
            team_name TEXT,
            elo_rating INTEGER,
            form REAL,
            matches_played INTEGER,
            matches_won INTEGER,
            matches_lost INTEGER,
            matches_tied INTEGER,
            is_provisional BOOLEAN,
            provisional_avg_elo REAL
        )
    """)   

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rankings(
            team_name TEXT,
            rank INTEGER,
            PRIMARY KEY (team_name, rank)
        )
    """)

    conn.commit()

    conn.close()

if __name__ == "__main__":
    results = load_data()
    results["match_winner"] = results.apply(get_winner, axis=1)
    results["goal_diff"] = results.apply(get_goal_diff, axis=1)

    results = results.drop(columns = ["winner", "first_shooter"])

    results = remove_tournaments("tournament_blacklist.txt", results)
    results = remove_teams("fifa_teams.txt", results)

    results.to_csv(DATA_PATH / "final_results.csv", index=False)

    build_database(results)
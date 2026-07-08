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

def get_goal_dif(row: pd.Series) -> int:

    if pd.isna(row["match_winner"]):

        return 0

    elif row["match_winner"] == row["home_team"]:

        return row["home_score"] - row["away_score"]

    elif row["match_winner"] == row["away_team"]:

        return row["away_score"] - row["home_score"]

def build_database(results: pd.DataFrame) -> None:
    conn = sqlite3.connect(PARENT_PATH / "src" / "world_football_elo" / "data" / "international_football_data.db")
    cursor = conn.cursor()

    results.to_sql("matches", conn, if_exists="replace", index=False)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teams(
            team_name TEXT PRIMARY KEY,
            matches_played INTEGER DEFAULT 0,
            is_provisional BOOLEAN DEFAULT 1,
            current_elo REAL DEFAULT 1000.0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS snapshots(
            date TEXT,
            team_name TEXT,
            elo_rating REAL,
            form_delta REAL
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
    results["goal_dif"] = results.apply(get_goal_dif, axis=1)

    results = results.drop(columns = ["winner", "first_shooter"])

    results.to_csv(DATA_PATH / "final_results.csv", index=False)

    build_database(results)
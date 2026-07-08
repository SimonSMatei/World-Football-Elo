import sqlite3
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "international_football_data.db"

def load_matches(start_date: str | None = None, end_date: str | None = None) -> pd.DataFrame:
    conn = sqlite3.connect(DATA_PATH)

    
    conditions = []
    parms = []

    query = "SELECT * FROM matches"
    
    if start_date is not None:
        conditions.append("date >= ?")
        parms.append(start_date)
    
    if end_date is not None:
        conditions.append("date <= ?")
        parms.append(end_date)
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)


    matches = pd.read_sql(query, conn, params = parms)

    conn.close()

    return matches
    
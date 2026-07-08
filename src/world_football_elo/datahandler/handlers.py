import sqlite3
import pandas as pd
from pathlib import Path

def load_matches(data_path: Path, start_date: str | None = None, end_date: str | None = None) -> pd.DataFrame:
    conn = sqlite3.connect(data_path)

    
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
    
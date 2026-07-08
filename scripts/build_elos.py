from world_football_elo import Country, load_matches
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "src" / "world_football_elo" / "data" / "international_football_data.db"

MATCHES = load_matches(DATA_PATH)

if __name__ == "__main__":
    pass
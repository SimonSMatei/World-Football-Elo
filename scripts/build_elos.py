from world_football_elo import Country, load_matches

MATCHES = load_matches(start_date = "2000-01-01", end_date = "2000-02-01")

if __name__ == "__main__":
    print(MATCHES)
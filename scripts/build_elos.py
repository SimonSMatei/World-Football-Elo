import world_football_elo as wf

MATCHES = wf.load_matches(start_date = "2000-01-01", end_date = "2026-06-10")

if __name__ == "__main__":
    countries = {}

    for match in MATCHES.itertuples():
        match_info = {
            "home_team": match.home_team,
            "away_team": match.away_team,
            "match_winner": match.match_winner,
            "date": match.date,
            "goal_diff": match.goal_diff,
            "tournament": match.tournament,
            "neutral": match.neutral
        }
        
        wf.update_elo(match_info, countries)
    
    countries = wf.get_standings(countries)
    
    rank = 1

    file = ".\\rankings.txt"

    with open(file, "w", encoding="utf-8") as f:
        for key, value in countries.items():
            f.write(f"{rank} - Country: {key} \t Elo: {value.elo}\n")
            rank += 1
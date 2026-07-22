def _validate_user_input(match_info: dict) -> None:
    if "home_team" not in match_info.keys():
        raise ValueError("Every match must have a home team listed")
    elif "away_team" not in match_info.keys():
        raise ValueError("Every match must have an away team listed")
    elif "match_winner" not in match_info.keys():
        raise ValueError("Every match must have a match winner listed")
    elif "date" not in match_info.keys():
        raise ValueError("Every match must have a date listed")
    elif "goal_diff" not in match_info.keys():
        raise ValueError("Every match must have a goal difference listed")

def get_standings(countries: dict) -> dict:
    """
    Sorts the dictionary of Country objects by their current Elo rating.
    Returns a new dictionary ordered from highest Elo to lowest.
    """
    return dict(sorted(countries.items(), key=lambda item: item[1].elo, reverse=True))
from .country import Country
from ..utils import _validate_user_input

def update_elo(match_info: dict, countries: dict, provisional_date: str = "2000-12-31") -> None:
    
    _validate_user_input(match_info)

    date = match_info["date"]

    goal_diff = match_info["goal_diff"]

    if "tournament" in match_info.keys():
        tournament = match_info["tournament"]
    else:
        tournament = None
    
    if "neutral" in match_info.keys():
        neutral_site = match_info["neutral"]
    else:
        neutral_site = False

    match_winner = match_info["match_winner"]

    if match_info["home_team"] not in countries.keys():
        home_team = Country(match_info["home_team"])

        if date > provisional_date:
            home_team.is_provisional = True
    else:
        home_team = countries[match_info["home_team"]]

    if match_info["away_team"] not in countries.keys():
        away_team = Country(match_info["away_team"])

        if date > provisional_date:
            away_team.is_provisional = True
    else:
        away_team = countries[match_info["away_team"]]
    
    
    if away_team.is_provisional or home_team.is_provisional:
        home_team.matches_played += 1
        away_team.matches_played += 1

        if match_winner == home_team.name:
            home_team.matches_won += 1
            away_team.matches_lost += 1
        elif match_winner == away_team.name:
            home_team.matches_lost += 1
            away_team.matches_won += 1
        else:
            home_team.matches_tied += 1
            away_team.matches_tied += 1

        if away_team.is_provisional:
            away_team.provisional_avg_elo = (away_team.provisional_avg_elo * (away_team.matches_played - 1) + home_team.elo) / (away_team.matches_played)
        
            if away_team.matches_played >= 5:
                away_team.elo = away_team.provisional_avg_elo + 400 * ((away_team.matches_won - away_team.matches_lost) / 5)
                
                away_team.is_provisional = False

        if home_team.is_provisional:
            home_team.provisional_avg_elo = (home_team.provisional_avg_elo * (home_team.matches_played - 1) + away_team.elo) / (home_team.matches_played)
        
            if home_team.matches_played >= 5:
                home_team.elo = home_team.provisional_avg_elo + 400 * ((home_team.matches_won - home_team.matches_lost) / 5)
                
                home_team.is_provisional = False
    else:
        if not neutral_site:
            home_field_adv = 100
        else:
            home_field_adv = 0

        exp_home = 1 / (1 + 10 ** ((away_team.elo - (home_team.elo + home_field_adv)) / 400))

        if goal_diff <= 1:
            g = 1
        elif goal_diff == 2:
            g = 1.5
        else:
            g = (11 + goal_diff) / 8

        if tournament is not None:
            major_tournaments = ["UEFA Euro", "Copa América", "African Cup of Nations", "Gold Cup", "AFC Asian Cup", "Oceania Nations Cup"]

            major_qualification = [i + " qualification" for i in major_tournaments]

            if tournament == "FIFA World Cup":
                k = 60
            elif tournament in major_tournaments:
                k = 50
            elif tournament in major_qualification:
                k = 40
            elif tournament == "Friendly":
                k = 20
            else:
                k = 30
        else:
            k = 20
    
        if match_winner == home_team.name:
            w_home = 1
            
            home_team.matches_won += 1
            away_team.matches_lost += 1

        elif match_winner == away_team.name: 
            w_home = 0

            home_team.matches_lost += 1
            away_team.matches_won += 1

        else:
            w_home = 0.5

            home_team.matches_tied += 1
            away_team.matches_tied += 1

        delta = k * g * (w_home - exp_home)

        delta = round(delta)

        home_team.elo += delta
        away_team.elo -= delta
        
        home_team.form = (delta * 0.2) + (home_team.form * (0.8))
        away_team.form = (-1 * delta * 0.2) + (away_team.form * (0.8))

        home_team.matches_played += 1
        away_team.matches_played += 1
        
    countries[home_team.name] = home_team
    countries[away_team.name] = away_team
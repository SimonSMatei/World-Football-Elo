class Country:
    
    def __init__(self, 
                 name: str, 
                 elo: int = 1000, 
                 matches_played: int = 0,
                 matches_won: int = 0,
                 matches_lost: int = 0,
                 matches_tied: int = 0,
                 form: float = 0.0,
                 is_active: bool = True,
                 is_provisional: bool = False,
                 provisional_avg_elo: float = 0.0) -> None:
        
        self.name = name

        self.elo = elo

        if matches_played != matches_won + matches_tied + matches_lost:
            raise ValueError("Team record must match the number of matches played")

        self.matches_played = matches_played

        self.matches_won = matches_won

        self.matches_lost = matches_lost

        self.matches_tied = matches_tied

        self.form = form

        self.is_active = is_active

        self.is_provisional = is_provisional

        self.provisional_avg_elo = provisional_avg_elo



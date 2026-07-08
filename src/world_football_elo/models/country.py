

class Country:
    
    def __init__(self, 
                 name: str, 
                 elo: int = 1000, 
                 matches_played: int = 0) -> None:
        
        self.name = name

        self.elo = elo

        self.matches_played = matches_played
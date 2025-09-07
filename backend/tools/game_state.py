
# game_state.py
class GameState:
    def __init__(self):
        self.npcs = []
        self.players = []
        self.turn = 1
        self.day = 1
        self.weather = "clear"
        self.current_phase = "exploration" # can be "combat", "exploration", or "interaction"
        self.current_location = "dark forest"
        self.locations = [self.current_location]
        self.objectives = []

    def init_player(self, name: str, character_class: str, race: str):
        self.players = {
            "name": name,
            "class": character_class,
            "race": race,
            "hp": 100,
            "inventory": []
        }

    def add_npc(self, npc):
        """Add an NPC object to the npcs list."""
        self.npcs.append(npc)

    def __repr__(self):
        return (f"GameState(npcs={self.npcs}, players={self.players}, turn={self.turn}, "
                f"day={self.day}, weather={self.weather!r}, objectives={self.objectives})")

game_state = GameState()
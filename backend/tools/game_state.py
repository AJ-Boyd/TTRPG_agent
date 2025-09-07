from .character import Character

ex_char = Character(
    playable=True,
    name="Jimmy the Hero",
    race="Human",
    class_type="Ranger",
    alignment="Neutral Good",
    strength=16,
    dexterity=14,
    intelligence=12,
    constitution=15,
    wisdom=13,
    charisma=10,
    speed=30,
    hp=15,
    hit_dice=10,
    mood=5,
    # Ranger skill proficiencies (proficiency bonus +2 at level 1)
    athletics=2,          # Proficient, for climbing and swimming in forest
    stealth=2,           # Proficient, key ranger skill
    survival=2,          # Proficient, for tracking and foraging
    perception=0,        # Not proficient, but important for spotting danger
    animal_handling=0,   # Not proficient
    nature=0,           # Not proficient
    acrobatics=0,       # Not proficient
    arcana=0,           # Not proficient
    deception=0,        # Not proficient
    history=0,          # Not proficient
    insight=0,          # Not proficient
    intimidation=0,     # Not proficient
    investigation=0,    # Not proficient
    medicine=0,         # Not proficient
    performance=0,      # Not proficient
    persuasion=0,       # Not proficient
    religion=0,         # Not proficient
    sleight_of_hand=0,  # Not proficient
    # Combat abilities
    attacks=["Longsword (1d8 piercing)", "Shortbow (1d6 piercing)"],
    spells=[],  # Rangers don't get spells at level 1
    resistances=[],  # No special resistances at level 1
    vulnerabilities=[]  # No vulnerabilities
)

# game_state.py
class GameState:
    def __init__(self):
        self.npcs = []
        self.players = [ex_char]
        self.turn = 1
        self.day = 1
        self.weather = "clear"
        self.current_phase = "exploration" # can be "combat", "exploration", or "interaction"
        self.current_location = "dark forest"
        self.locations = [self.current_location]
        self.objectives = [
            "Navigate through the dark forest filled with dangers and creatures",
            "Find and follow the mountain trail leading to the hidden cave",
            "Locate Eldrin the Wizard and earn his trust for guidance",
            "Avoid or overcome various traps along the path",
            "Discover the location of the hidden cave",
            "Retrieve the ancient treasures from the cave",
            "Handle any guardians or protectors of the treasure",
            "Successfully return with the treasures",
            # Secondary objectives that can be discovered
            "Map out safe paths through the forest",
            "Learn about the forest's history from Eldrin",
            "Discover the true nature of the ancient treasures",
            "Find out why the cave and its treasures were hidden"
        ]

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
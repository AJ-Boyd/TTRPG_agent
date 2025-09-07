"""
auth: AJ Boyd
date: 7/30/2025
desc: Character class definition for TTRPG agent.
"""

class Character:
    def __init__(self, playable:bool, name: str, race: str, class_type: str, alignment: str,
                 strength: int, dexterity: int, intelligence: int,
                 constitution: int, wisdom: int, charisma: int, hp: int, hit_dice: int, mood: int, speed: int = 30,
                 acrobatics: int = 0, animal_handling: int = 0, arcana: int = 0,
                 athletics: int = 0, deception: int = 0, history: int = 0,
                 insight: int = 0, intimidation: int = 0, investigation: int = 0,
                 medicine: int = 0, nature: int = 0, perception: int = 0,
                 performance: int = 0, persuasion: int = 0, religion: int = 0,
                 sleight_of_hand: int = 0, stealth: int = 0, survival: int = 0, 
                 attacks: list = [],
                 spells: list = [], resistances: list = [],
                 vulnerabilities: list = []):
        # basic attributes
        self.playable = playable
        self.name = name
        self.race = race
        self.class_type = class_type
        self.alignment = alignment
        # stats and modifiers
        self.stats = {
            "strength": strength,
            "dexterity": dexterity,
            "intelligence": intelligence,
            "constitution": constitution,
            "wisdom": wisdom,
            "charisma": charisma,
        }
        self.stat_modifiers = {
            "strength": (strength - 10) // 2,
            "dexterity": (dexterity - 10) // 2,
            "intelligence": (intelligence - 10) // 2,
            "constitution": (constitution - 10) // 2,
            "wisdom": (wisdom - 10) // 2,
            "charisma": (charisma - 10) // 2,
        }
        # combat attributes
        self.speed = speed
        self.hp = hp
        self.max_hp = hp
        self.hit_dice = hit_dice
        self.attacks = attacks if attacks is not None else []
        self.spells = spells if spells is not None else []
        # skill proficiencies and modifiers
        # Each skill is a tuple of (base_stat, proficiency_bonus)
        self.skills = {
            # Strength-based skills
            "athletics": (self.stat_modifiers["strength"], athletics),
            
            # Dexterity-based skills
            "acrobatics": (self.stat_modifiers["dexterity"], acrobatics),
            "sleight_of_hand": (self.stat_modifiers["dexterity"], sleight_of_hand),
            "stealth": (self.stat_modifiers["dexterity"], stealth),
            
            # Intelligence-based skills
            "arcana": (self.stat_modifiers["intelligence"], arcana),
            "history": (self.stat_modifiers["intelligence"], history),
            "investigation": (self.stat_modifiers["intelligence"], investigation),
            "nature": (self.stat_modifiers["intelligence"], nature),
            "religion": (self.stat_modifiers["intelligence"], religion),
            
            # Wisdom-based skills
            "animal_handling": (self.stat_modifiers["wisdom"], animal_handling),
            "insight": (self.stat_modifiers["wisdom"], insight),
            "medicine": (self.stat_modifiers["wisdom"], medicine),
            "perception": (self.stat_modifiers["wisdom"], perception),
            "survival": (self.stat_modifiers["wisdom"], survival),
            
            # Charisma-based skills
            "deception": (self.stat_modifiers["charisma"], deception),
            "intimidation": (self.stat_modifiers["charisma"], intimidation),
            "performance": (self.stat_modifiers["charisma"], performance),
            "persuasion": (self.stat_modifiers["charisma"], persuasion),
        }
        
        # status effects
        self.conditions = []
        self.resistances = resistances if resistances is not None else []
        self.vulnerabilities = vulnerabilities if vulnerabilities is not None else []
        # social attributes
        self.mood = mood

    def get_skill_modifier(self, skill_name: str) -> int:
        """
        Calculate the total modifier for a skill including ability modifier and proficiency.
        Args:
            skill_name (str): The name of the skill to get the modifier for
        Returns:
            int: The total modifier for the skill
        """
        if skill_name not in self.skills:
            raise ValueError(f"Unknown skill: {skill_name}")
        
        ability_mod, prof_bonus = self.skills[skill_name]
        return ability_mod + prof_bonus

    def is_proficient(self, skill_name: str) -> bool:
        """
        Check if the character is proficient in a skill.
        Args:
            skill_name (str): The name of the skill to check
        Returns:
            bool: True if the character is proficient in the skill, False otherwise
        """
        if skill_name not in self.skills:
            raise ValueError(f"Unknown skill: {skill_name}")
        
        return self.skills[skill_name][1] > 0

    def __repr__(self):
        basic_info = (
            f"\nCharacter Information:\n"
            f"==================\n"
            f"Basic Attributes:\n"
            f"- Name: {self.name}\n"
            f"- Race: {self.race}\n"
            f"- Class: {self.class_type}\n"
            f"- Alignment: {self.alignment}\n"
            f"- Playable: {self.playable}\n\n"
            
            f"Combat Stats:\n"
            f"- HP: {self.hp}/{self.max_hp}\n"
            f"- Speed: {self.speed}\n"
            f"- Hit Dice: d{self.hit_dice}\n"
            f"- Attacks: {', '.join(str(a) for a in self.attacks) if self.attacks else 'None'}\n"
            f"- Spells: {', '.join(str(s) for s in self.spells) if self.spells else 'None'}\n\n"
            
            f"Ability Scores:\n"
            f"- Strength: {self.stats['strength']} (Mod: {self.stat_modifiers['strength']})\n"
            f"- Dexterity: {self.stats['dexterity']} (Mod: {self.stat_modifiers['dexterity']})\n"
            f"- Constitution: {self.stats['constitution']} (Mod: {self.stat_modifiers['constitution']})\n"
            f"- Intelligence: {self.stats['intelligence']} (Mod: {self.stat_modifiers['intelligence']})\n"
            f"- Wisdom: {self.stats['wisdom']} (Mod: {self.stat_modifiers['wisdom']})\n"
            f"- Charisma: {self.stats['charisma']} (Mod: {self.stat_modifiers['charisma']})\n\n"
            
            f"Skills:\n"
        )
        
        # Add all skills, grouped by ability score
        skills_by_ability = {
            "Strength": ["athletics"],
            "Dexterity": ["acrobatics", "sleight_of_hand", "stealth"],
            "Intelligence": ["arcana", "history", "investigation", "nature", "religion"],
            "Wisdom": ["animal_handling", "insight", "medicine", "perception", "survival"],
            "Charisma": ["deception", "intimidation", "performance", "persuasion"]
        }
        
        skills_info = ""
        for ability, skill_list in skills_by_ability.items():
            skills_info += f"{ability}-based skills:\n"
            for skill in skill_list:
                mod = self.get_skill_modifier(skill)
                prof = "✓" if self.is_proficient(skill) else "✗"
                skills_info += f"  - {skill.replace('_', ' ').title()}: {mod:+d} ({prof})\n"
            skills_info += "\n"
        
        status_info = (
            f"Status Effects:\n"
            f"- Conditions: {', '.join(self.conditions) if self.conditions else 'None'}\n"
            f"- Resistances: {', '.join(self.resistances) if self.resistances else 'None'}\n"
            f"- Vulnerabilities: {', '.join(self.vulnerabilities) if self.vulnerabilities else 'None'}\n\n"
            f"Social:\n"
            f"- Mood: {self.mood}\n"
        )
        
        return basic_info + skills_info + status_info

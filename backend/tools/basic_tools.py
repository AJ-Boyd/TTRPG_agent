"""
auth: AJ Boyd
date: 7/30/2025
desc: holds basic gameplay tools for TTRP                    # Combat and special abilities
                    attacks: list[str] = [], spells: list[str] = [],
                    resistances: list[str] = [], vulnerabilities: list[str] = []) -> Character:gent.
"""
import random
from .character import Character
from .game_state import game_state

def attack():
    game_state["player"]["hp"] -= 5
    return game_state["player"]["hp"]
                  
def calculator(expression: str) -> float:
    """
    Evaluates a mathematical expression and returns the result.
    Args:
        expression (str): The mathematical expression to evaluate.
    Returns:
        float: The result of the evaluated expression.
    """
    try:
        # Safely evaluate the expression
        result = eval(expression, {"__builtins__": None}, {})
        if not isinstance(result, (int, float)):
            raise ValueError("Expression did not evaluate to a number.")
        return result
    except Exception as e:
        raise ValueError(f"Invalid expression: {expression}. Error: {e}")

def roll_dice(n: int = 1, sides: int = 20) -> list[int]:
    """
    Simulates rolling a dice with the given number of sides (default 20).
    Args:
        n (int): The number of dice to roll.
        sides (int): The number of sides on the dice (default 20).
    Returns:
        list[int]: A list of random integers between 1 and the number of sides.
    """
    if n < 1:
        raise ValueError("Number of dice must be at least 1.")
    
    rolls = [random.randint(1, sides) for _ in range(n)]
    return rolls

def roll_stat(stat: str) -> int:
    """
    When the player wants to perform an action that may result in failure, roll a skill check.
    Args:
        stat (str): The name of the stat to roll.
    Returns:
        int: A random integer representing the rolled stat.
    """
    return roll_dice(20)

def read_objectives() -> list[str]:
    """
    Returns the current objectives from the game state.
    """
    return game_state.objectives

def read_players() -> list[Character]:
    """
    Returns the current players from the game state.
    """
    return game_state.players

def create_character(is_player: bool, name: str, race: str, class_type: str, alignment: str,
                    strength: int, dexterity: int, intelligence: int,
                    constitution: int, wisdom: int, charisma: int, speed: int,
                    hp: int, hit_dice: int, mood: int,
                    # Skill proficiencies
                    acrobatics: int = 0, animal_handling: int = 0, arcana: int = 0,
                    athletics: int = 0, deception: int = 0, history: int = 0,
                    insight: int = 0, intimidation: int = 0, investigation: int = 0,
                    medicine: int = 0, nature: int = 0, perception: int = 0,
                    performance: int = 0, persuasion: int = 0, religion: int = 0,
                    sleight_of_hand: int = 0, stealth: int = 0, survival: int = 0,
                    # Combat and special abilities
                    attacks: list[dict[str, str | int]] = [], 
                    spells: list[dict[str, str | int]] = [],
                    resistances: list[dict[str, str]] = [], 
                    vulnerabilities: list[dict[str, str]] = []) -> Character:
    """
    Creates a character (player or NPC) with the given attributes.
    Args:
        is_player (bool): Whether this is a player character (True) or NPC (False)
        name (str): The name of the character
        race (str): The race of the character
        class_type (str): The class of the character
        attacks (list[dict]): List of attack dictionaries with name, damage, and type
        spells (list[dict]): List of spell dictionaries with name, level, and school
        resistances (list[dict]): List of damage resistance dictionaries with type and description
        vulnerabilities (list[dict]): List of vulnerability dictionaries with type and description
        alignment (str): The alignment of the character
        strength (int): The strength score
        dexterity (int): The dexterity score
        intelligence (int): The intelligence score
        constitution (int): The constitution score
        wisdom (int): The wisdom score
        charisma (int): The charisma score
        speed (int): Movement speed in feet
        hp (int): Current hit points
        hit_dice (int): Type of hit dice (e.g., 6 for d6, 8 for d8)
        mood (int): Character's disposition value
        
        # Skill proficiencies (all default to 0 for no proficiency)
        acrobatics (int): Proficiency in Acrobatics (DEX)
        animal_handling (int): Proficiency in Animal Handling (WIS)
        arcana (int): Proficiency in Arcana (INT)
        athletics (int): Proficiency in Athletics (STR)
        deception (int): Proficiency in Deception (CHA)
        history (int): Proficiency in History (INT)
        insight (int): Proficiency in Insight (WIS)
        intimidation (int): Proficiency in Intimidation (CHA)
        investigation (int): Proficiency in Investigation (INT)
        medicine (int): Proficiency in Medicine (WIS)
        nature (int): Proficiency in Nature (INT)
        perception (int): Proficiency in Perception (WIS)
        performance (int): Proficiency in Performance (CHA)
        persuasion (int): Proficiency in Persuasion (CHA)
        religion (int): Proficiency in Religion (INT)
        sleight_of_hand (int): Proficiency in Sleight of Hand (DEX)
        stealth (int): Proficiency in Stealth (DEX)
        survival (int): Proficiency in Survival (WIS)
        
        # Combat and special abilities
        attacks (list): List of attacks the character can perform
        spells (list): List of spells the character knows
        resistances (list): Damage types the character is resistant to
        vulnerabilities (list): Damage types the character is vulnerable to
        
    Returns:
        Character: A new Character instance with the specified attributes
        speed (int): The speed
        hp (int): The hit points
        hit_dice (int): The hit dice
        mood (int): The character's mood, affecting interactions
        attacks (list): A list of attacks the character can perform
        spells (list): A list of spells the character can cast
        resistances (list): A list of damage types the character is resistant to
        vulnerabilities (list): A list of damage types the character is vulnerable to
    Returns:
        Character: A Character object representing the created character.
    """
    character = Character(
        playable=is_player,
        name=name,
        race=race,
        class_type=class_type,
        alignment=alignment,
        strength=strength,
        dexterity=dexterity,
        intelligence=intelligence,
        constitution=constitution,
        wisdom=wisdom,
        charisma=charisma,
        speed=speed,
        hp=hp,
        hit_dice=hit_dice,
        mood=mood,
        # Skill proficiencies
        acrobatics=acrobatics,
        animal_handling=animal_handling,
        arcana=arcana,
        athletics=athletics,
        deception=deception,
        history=history,
        insight=insight,
        intimidation=intimidation,
        investigation=investigation,
        medicine=medicine,
        nature=nature,
        perception=perception,
        performance=performance,
        persuasion=persuasion,
        religion=religion,
        sleight_of_hand=sleight_of_hand,
        stealth=stealth,
        survival=survival,
        # Combat and special abilities
        attacks=attacks if attacks is not None else [],
        spells=spells if spells is not None else [],
        resistances=resistances if resistances is not None else [],
        vulnerabilities=vulnerabilities if vulnerabilities is not None else []
    )

    print(f"Created character: {repr(character)},")
    if is_player:
        game_state.players.append(character)
    else:
        game_state.add_npc(character)
    
    return character

def set_character_property(chacter_name: str, property: str, value) -> None:
    """
    Sets a property of a character (player or NPC) to a new value.
    Args:
        character_name (str): The name of the character to modify
        property (str): The property to set (e.g., "hp", "mood", "stats['strength']")
        value: The new value to assign to the property
    """
    for char in game_state.players + game_state.npcs:
        if char.name == chacter_name:
            if property.startswith("stats["):
                stat_name = property.split("[")[1].strip("]'\"")
                if stat_name in char.stats:
                    char.stats[stat_name] = value
                    char.stat_modifiers[stat_name] = (value - 10) // 2
            elif hasattr(char, property):
                setattr(char, property, value)
            else:
                raise ValueError(f"Property {property} not found on character {chacter_name}.")
            return
    raise ValueError(f"Character {chacter_name} not found.")


def roll_stats(stat: str) -> dict[str, int]:
    """
    Rolls 4d6 for each stat and returns the highest 3 rolls. The player can use this to generate their stats.
    """
    dice_rolls = sorted(roll_dice(4, 6), reverse=True)
    return {stat: sum(dice_rolls[:3])}
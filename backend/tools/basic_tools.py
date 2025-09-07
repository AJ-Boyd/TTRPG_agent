"""
auth: AJ Boyd
date: 7/30/2025
desc: holds basic gameplay tools for TTRPG agent.
"""
import random
from tools.game_state import game_state

def attack():
    game_state["player"]["hp"] -= 5
    return game_state["player"]["hp"]

class NPC:
    def __init__(self, name: str, race: str, class_type: str, alignment: str,
                 strength: int, dexterity: int, intelligence: int,
                 constitution: int, wisdom: int, charisma: int, speed: int,
                 hp: int, hit_dice: int, mood: int, spells: list = None):
        self.name = name
        self.race = race
        self.class_type = class_type
        self.alignment = alignment
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
        self.speed = speed
        self.hp = hp
        self.hit_dice = hit_dice
        self.mood = mood
        self.spells = spells if spells is not None else []

    def __repr__(self):
        return (f"NPC(name={self.name!r}, race={self.race!r}, class_type={self.class_type!r}, "
                f"alignment={self.alignment!r}, stats={self.stats}, speed={self.speed}, "
                f"hp={self.hp}, hit_dice={self.hit_dice}, spells={self.spells})")
    
class Player(NPC):
    def __init__(self, name: str, race: str, class_type: str, alignment: str,
                 strength: int, dexterity: int, intelligence: int,
                 constitution: int, wisdom: int, charisma: int, speed: int,
                 hp: int, hit_dice: int, mood: int, spells: list[str] = None,
                 equipment: list[str] = None, armor_class: int = 10,
                 skills: list[str] = None, tool_proficiencies: list[str] = None,
                 saving_throws: list[str] = None, traits: list[str] = None):
        super().__init__(name, race, class_type, alignment,
                         strength, dexterity, intelligence,
                         constitution, wisdom, charisma, speed,
                         hp, hit_dice, mood, spells)
        self.equipment = equipment if equipment is not None else []
        self.armor_class = armor_class
        self.skills = skills if skills is not None else []
        self.tool_proficiencies = tool_proficiencies if tool_proficiencies is not None else []
        self.saving_throws = saving_throws if saving_throws is not None else []
        self.traits = traits if traits is not None else []

    def __repr__(self):
        return (f"Player(name={self.name!r}, race={self.race!r}, class_type={self.class_type!r}, "
                f"alignment={self.alignment!r}, stats={self.stats}, speed={self.speed}, hp={self.hp}, "
                f"hit_dice={self.hit_dice}, mood={self.mood}, spells={self.spells}, equipment={self.equipment}, "
                f"armor_class={self.armor_class}, skills={self.skills}, tool_proficiencies={self.tool_proficiencies}, "
                f"saving_throws={self.saving_throws}, traits={self.traits})")
    
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
    Rolls a stat based on the stat name.
    Args:
        stat (str): The name of the stat to roll.
    Returns:
        int: A random integer representing the rolled stat.
    """
    return roll_dice(20)

def create_npc(name: str, race: str, class_type: str, alignment: str, 
               strength: int, dexterity: int, intelligence: int, 
               constitution: int, wisdom: int, charisma:int, speed: int,
               HP: int, hit_dice: int, spells: list[str] = None) -> NPC:
    """
    Creates a non-player character (NPC) with the given attributes.
    Args:
        name (str): The name of the NPC
        race (str): The race of the NPC
        class_type (str): The class of the NPC
        alignment (str): The alignment of the NPC
        strength (int): The strength score of the NPC
        dexterity (int): The dexterity score of the NPC
        intelligence (int): The intelligence score of the NPC
        constitution (int): The constitution score of the NPC
        wisdom (int): The wisdom score of the NPC
        charisma (int): The charisma score of the NPC
        speed (int): The speed of the NPC
        HP (int): The hit points of the NPC
        hit_dice (int): The hit dice of the NPC
        mood (int): How much the NPC likes the player, affecting interactions
        spells (list): A list of spells the NPC can cast
    Returns:
        NPC: An NPC object representing the created NPC.
    """
    npc = NPC(
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
        hp=HP,
        hit_dice=hit_dice,
        spells=spells
    )

    game_state.add_npc(npc) # add npc to game state
    return npc


def create_player(name: str, race: str, class_type: str, alignment: str,
                 strength: int, dexterity: int, intelligence: int,
                 constitution: int, wisdom: int, charisma: int, speed: int,
                 hp: int, hit_dice: int, mood: int, spells: list[str] = None,
                 equipment: list[str] = None, armor_class: int = 10,
                 skills: list[str] = None, tool_proficiencies: list[str] = None,
                 saving_throws: list[str] = None, traits: list[str] = None) -> Player:
    """
    Creates a player character with the given attributes. Roll for stats to assign their values
    Args:
        name (str): The name of the player
        race (str): The race of the player
        class_type (str): The class of the player
        alignment (str): The alignment of the player
        strength (int): The strength score
        dexterity (int): The dexterity score
        intelligence (int): The intelligence score
        constitution (int): The constitution score
        wisdom (int): The wisdom score
        charisma (int): The charisma score
        speed (int): The speed
        hp (int): The hit points
        hit_dice (int): The hit dice
        mood (int): How much the player likes themselves, affecting interactions
        spells (list of str): A list of spells the player can cast
        equipment (list of str): Equipment carried by the player
        armor_class (int): The player's armor class
        skills (list of str): The player's skills
        tool_proficiencies (list of str): The player's tool proficiencies
        saving_throws (list of str): The player's saving throws
        traits (list of str): The player's traits
    Returns:
        Player: A Player object representing the created player.
    """
    player = Player(
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
        spells=spells,
        equipment=equipment,
        armor_class=armor_class,
        skills=skills,
        tool_proficiencies=tool_proficiencies,
        saving_throws=saving_throws,
        traits=traits
    )
    game_state.players.append(player)
    return player

def set_player_hp(player_name: str, new_hp: int) -> None:
    """
    Sets the player's HP to a new value.
    Args:
        player_name (str): The name of the player whose HP is being set.
        new_hp (int): The new HP value to set.
    """
    for player in game_state.players:
        if player.name == player_name:
            player.hp = new_hp
            return f"{player.name}'s HP updated to {new_hp}"
    return "Player not found."

def set_mood(npc_name: str, new_mood: int) -> None:
    """
    Sets the mood of an NPC to a new value.
    Args:
        npc_name (str): The name of the NPC whose mood is being set.
        new_mood (int): The new mood value to set.
    """
    for npc in game_state.npcs:
        if npc.name == npc_name:
            npc.mood = new_mood
            return f"{npc.name}'s mood updated to {new_mood}"
    return "NPC not found."


def roll_stats(stat: str) -> dict[str, int]:
    """
    Rolls 4d6 for each stat and returns the highest 3 rolls. The player can use this to generate their stats.
    """
    dice_rolls = sorted(roll_dice(4, 6), reverse=True)
    return {stat: sum(dice_rolls[:3])}
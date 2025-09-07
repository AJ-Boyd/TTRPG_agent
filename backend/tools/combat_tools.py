"""
auth: AJ Boyd
date: 7/30/2025
desc: holds the combat tools for TTRPG agent, including damage calculation and combat mechanics.
"""
from .basic_tools import roll_dice
from .game_state import game_state

def attack():
    game_state["player"]["hp"] -= 5
    return game_state["player"]["hp"]


def initiative(character_name: str) -> int:
    """
    Determines the initiative order for combat.
    """
    for npc in game_state.npcs:
        if npc.name == character_name:
            return roll_dice(1, 20)[0] + npc.stat_modifiers["dexterity"]
    for player in game_state.players:
        if player.name == character_name:
            return roll_dice(1, 20)[0] + player.stat_modifiers["dexterity"]

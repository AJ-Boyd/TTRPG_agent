"""
auth: AJ Boyd
date: 7/30/2025
desc: A simple TTRPG agent chatbot using LangGraph and Google Gemini.
"""

import dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from tools.basic_tools import roll_dice, create_npc, create_player, set_player_hp, set_mood
from tools.combat_tools import initiative
from tools.game_state import game_state

# Load environment variables from .env file
dotenv.load_dotenv(override=True)

# Set up Gemini model
gemini_api_key = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(api_key=gemini_api_key, model="gemini-2.5-flash")

# Define a simple tool
def greet_tool(name: str) -> str:
    """Greets the user by name."""
    return f"Hello, {name}! How can I assist you today?"

tools = [roll_dice, create_npc, create_player, set_player_hp, set_mood,
         initiative]

# Initialize the agent
agent = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=MemorySaver()
)
config = {"configurable": {"thread_id": "asdfasdfasdf"}}

# system prompt
messages = [{
    "role": "system",
    "content": """You are the Dungeon Master for a TTRPG game. You guide the player through the given story scenario.
    It is imperative the story maintain conflict. Do NOT allow the player to succeed without challenges. The story must be engaging and immersive, with rich descriptions and dynamic interactions.
    The story is open-ended and allows for player creativity and decision-making. The player can interact with the world, NPCs, and objects in various ways. Adjust the NPCs in the story to account for this.
    
    I will give you a scenario, and you will respond with the next part of the story. The player can then interact with the world, and you will adjust the story based on their actions.
    
    Scenario: The Player is in a dark forest surrounded by towering trees and the sounds of distant creatures. The air is thick with mist, and the path ahead is unclear. The player must navigate up a mountain trail to find a hidden cave rumored to hold ancient treasures. The player must be cautious, as the forest is known to be home to various creatures and traps that can hinder their progress.
    Create a Wizard NPC named "Eldrin" who is wise and knowledgeable about the forest. Eldrin can provide hints and guidance to the player, but he will not give away all the answers. The player must earn his trust to gain valuable information.

    Start by creating the player character with the user. They will start at level 1
    """
},
# {    "role": "user", "content": "begin prompted adventure."}
]

def run_agent(msg: str) -> str:
     # Agent responds first with the scenario
    # for step in agent.stream(
    #     {"messages": messages}, config, stream_mode="values"
    # ):
    #     step['messages'][-1].pretty_print()
    print(config)
    messages.append({"role": "user", "content": msg})
    response = agent.invoke({"messages": messages}, config)
    agent_msg = response['messages'][-1].content
    # print(agent_msg)
    messages.append({"role": "assistant", "content": agent_msg})
    return agent_msg
    # for step in agent.stream(
    #     {"messages": messages}, config, stream_mode="values"
    # ):
    #     step['messages'][-1].pretty_print()

      
# Example usage
if __name__ == "__main__":
    print("Welcome to the TTRPG Agent Chatbot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        # Ensure config includes a valid thread_id for the checkpointer
        response = run_agent(user_input)
        print(f"Agent: {response}")
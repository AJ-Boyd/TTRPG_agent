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
import tools.basic_tools as bt
import tools.combat_tools as ct
from tools.game_state import game_state

# Load environment variables from .env file
dotenv.load_dotenv(override=True)

# Set up Gemini model
gemini_api_key = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(api_key=gemini_api_key, model="gemini-2.5-flash")

tools = [bt.calculator, bt.create_character, bt.read_objectives, bt.read_players, bt.set_character_property,bt.roll_dice, ct.initiative]

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

    Start by reading the objectives and players. They will start at level 1.
    """
},
# {    "role": "user", "content": "begin prompted adventure."}
]

def run_agent(msg: str) -> str:
    # Append user message to conversation
    messages.append({"role": "user", "content": msg})
    
    # Get agent's response with tool usage tracking
    final_response = None
    
    for step in agent.stream({"messages": messages}, config, stream_mode="values"):
        # Print tool usage information
        if "actions" in step:
            for action in step["actions"]:
                tool_name = action[0]
                tool_args = action[1]
                print(f"\nTool Called: {tool_name}")
                print(f"Arguments: {tool_args}\n")
        if "messages" in step:
            # Print each new message as it comes in
            step['messages'][-1].pretty_print()
            final_response = step
    
    if not final_response:
        raise Exception("No response received from agent")
    
    # Get the final response
    agent_msg = final_response['messages'][-1].content
    
    # Append agent's response to conversation history
    messages.append({"role": "assistant", "content": agent_msg})
    
    return agent_msg

      
def export_conversation(filename: str = None) -> None:
    """
    Exports the conversation history to a text file.
    Args:
        filename (str, optional): The name of the file to export to. 
                                If None, generates a timestamp-based filename.
    """
    if filename is None:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.txt"
    
    filepath = os.path.join(os.getcwd(), "conversations", filename)
    
    # Create conversations directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("TTRPG Adventure Conversation Log\n")
        f.write("==============================\n\n")
        
        for msg in messages:
            role = msg["role"].title()
            content = msg["content"]
            
            if role == "System":
                f.write("Game Setup:\n")
                f.write("-----------\n")
            else:
                f.write(f"{role}:\n")
                f.write("-" * (len(role) + 1) + "\n")
            
            f.write(f"{content}\n\n")
        
        f.write("==============================\n")
        f.write("End of Conversation Log\n")
    
    print(f"\nConversation exported to: {filepath}")

# Example usage
if __name__ == "__main__":
    print("Welcome to the TTRPG Agent Chatbot!")
    print("Commands:")
    print("  'exit' or 'quit' - Exit the program")
    print("  'export' - Save conversation to file")
    print("  'export <filename>' - Save conversation to specific file")
    
    # Initial response to set up the scenario
    initial_response = run_agent("begin prompted adventure")
    
    # Main conversation loop
    while True:
        user_input = input("\nYou: ")
        
        # Handle commands
        if user_input.lower() in ("exit", "quit"):
            # Auto-export on exit
            export_conversation()
            print("Goodbye!")
            break
        elif user_input.lower().startswith("export"):
            # Handle export command
            parts = user_input.split(maxsplit=1)
            if len(parts) > 1:
                export_conversation(parts[1])
            else:
                export_conversation()
            continue
            
        try:
            response = run_agent(user_input)
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Please try again with a different input.")
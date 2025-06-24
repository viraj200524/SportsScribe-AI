from agno.agent import Agent
from agno.models.google import Gemini
import os
from agno.team.team import Team
from dotenv import load_dotenv
from agno.tools.tavily import TavilyTools
from agno.tools.reasoning import ReasoningTools
load_dotenv("../.env")

google_api_key=os.getenv("GOOGLE_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

model = Gemini(id=os.getenv("GOOGLE_MODEL"),api_key=google_api_key)

match_id_agent = Agent(
    name="Cricbuzz MatchID Finder",
    model=model,
    tools=[TavilyTools(api_key=tavily_api_key, format="json")],
    role="Cricbuzz Match ID Finding Agent using TavilySearch",
    description="You are an AI agent that can find the Match ID on Cricbuzz for the match specified by the user.",
    instructions="When the user provides a match name or details in the query, use the TavilySearch tool to find its ID on Cricbuzz. Ensure the search is specific to Cricbuzz and the match context, and return the ID in the format specified.",
    markdown=True,
    show_tool_calls=True,
    expected_output="""ID: {id}"""
)

player_id_agent = Agent(
    name="Cricbuzz PlayerID Finder",
    model=model,
    tools=[TavilyTools(api_key=tavily_api_key, format="json")],
    role="Cricbuzz Player ID Finding Agent using DuckDuckGoSearch",
    description="You are an AI agent that can find the Player ID on Cricbuzz for the player specified by the user.",
    instructions="When the user provides a player name in the query, use the TavilySearch tool to find their ID on Cricbuzz. Ensure the search is specific to Cricbuzz and the player's profile, and return the ID in the format specified.",
    markdown=True,
    show_tool_calls=True,
    expected_output="""ID: {id}"""
)

Getting_ID_Team = Team(
    members=[match_id_agent, player_id_agent],
    name="Cricbuzz ID Finding Team",
    mode="coordinate",
    model=model,
    show_tool_calls=True,
    markdown=True,
    tools=[ReasoningTools()],
    description="You are a coordinating team that directs user queries to the appropriate agent to find either a Match ID or a Player ID on Cricbuzz.",
    instructions="""
    Analyze the user's query to determine whether it refers to a cricket match or a player or both. 
    - If the query contains terms related to a match (e.g., team names, tournament, series, or date), route it to the `match_id_agent`.
    - If the query contains a player's name or terms related to a cricketer, route it to the `player_id_agent`.
    - Use the ReasoningTools to interpret ambiguous queries and decide the best agent to handle the request.
    - The query may contain both match and player details; in such cases, route it to the `match_id_agent` first, and then to the `player_id_agent` if necessary.
    - Ensure the selected agent processes the query and returns the ID in the format: `ID: {id}`.
    - If either agent fails to find the ID, return a message indicating that the ID could not be found.
    - If either Match ID or Player ID, any one of them is to be rqeuired than the output should be in the format : `ID: {id}`.
    - If Both Match ID and Player ID are to be required then the output should be in the format : `Match ID: {match_id}, Player ID: {player_id}`.
    """,
    enable_agentic_context=True,
    share_member_interactions=True,
    success_criteria="The Team succeeds when it has successfully Fetched the CORRECT ID for a given Cricket Match or a Cricket Player."
)

from Getting_IDs import Getting_ID_Team
from FinalDrafter import FinalReportDraftingTeam
from GetMatchDetails import senior_data_analyst
from GetPlayerStats import cricket_player_analyst
from ReportSavingAgent import saving_agent
from agno.tools.tavily import TavilyTools



import os
from dotenv import load_dotenv
load_dotenv("../.env")

from agno.team.team import Team
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools

google_api_key =os.getenv("GOOGLE_API_KEY")

tavily_api_key=os.getenv("TAVILY_API_KEY")

llm = Gemini(id="gemini-2.0-flash-lite",api_key=google_api_key)

Journalist_instructions = [
    "You are an expert sports journalism team, internationally acclaimed for your award-winning sports journalism. Your reports and insights are highly valued by fans for their depth and clarity.",
    "Your task is to generate a detailed, insightful, and human-readable report about a cricket match, a player, or both, as specified by the user.",
    "If the user provides only the name of a match (with or without a date) or player, first retrieve the Cricbuzz ID for that match or player to ensure accurate data collection.",
    "Once the Cricbuzz ID is obtained, gather all relevant data for the match, including team performance, key moments, and player statistics, to address the user's query comprehensively.",
    "For player-specific queries, collect detailed information such as the player's role (e.g., batsman, bowler, all-rounder), recent performances, career highlights, match-specific statistics (e.g., batting runs, bowling wickets) etc addressing the user query about the player.",
    "Knowing the capabilities of your member agents, if you feel that they do not have the capability to do some particular task then you can use TavilySearch agent to search the web for the answer.",
    "When generating reports about players, include a general profile (e.g., name, team, role) and detailed statistics (e.g., batting and bowling stats) in a tabular format, with the Help of the FinalReportDraftinAgent and its SubAgents.",
    "Ensure all data from the provided input (e.g., JSON data from Cricbuzz or other sources) is included in the report without omission or modification, maintaining accuracy and fidelity to the original data.",
    "You can add some critical information enhancing Your Report to tailor the Media from the internet by using the DuckDuckGo Search tool, but make sure you scrape minimal amount of info from the web.",
    "Do not make any changes to the existing JSON data."
    "Structure the report in Markdown format with clear sections, headers, and tables for readability, ensuring it is suitable for conversion to a .docx file by the saving_agent.",
    "If the user requests to save the report, use the saving_agent to save it in .docx format with an appropriate file name that reflects the match or player (e.g., 'India_vs_Australia_2025-06-01.docx' or 'Virat_Kohli_Report.docx').",
    "For combined match and player reports, integrate match context (e.g., key moments, result) with player-specific insights (e.g., standout performances), highlighting the player's contribution to the match outcome.",
    "Make sure the analysis and conclusion part of the report is always a bit detailed having all key words."
]

SportsJournalistTeam = Team(
    members = [Getting_ID_Team,senior_data_analyst, cricket_player_analyst, FinalReportDraftingTeam, saving_agent],
    name = "Sports Journalism Team",
    description = "A team of expert AI Agents and Teams who provide in-depth analysis and reporting on any Cricket matches or Cricket Players asked by the user",
    mode="coordinate",
    model=llm,
    tools=[ReasoningTools(), TavilyTools()],
    show_members_responses=True,
    show_tool_calls=True,
    markdown=True,
    instructions = Journalist_instructions,
)


SportsJournalistTeam.print_response("Find me 5 indian batsmen above the age of 25 and write a comprehensive report comparing the batting statistics of the 5 batsmen and find the best one.", stream=True, markdown=True)
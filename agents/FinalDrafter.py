from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools import Toolkit
from agno.tools.reasoning import ReasoningTools
from agno.tools.tavily import TavilyTools
from agno.team import Team
import os
from dotenv import load_dotenv
from agno.models.huggingface import HuggingFace

# Load environment variables
load_dotenv("../.env")

google_api_key = os.getenv("GOOGLE_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
token = os.getenv("HF_TOKEN")

# Validate environment variables
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY not found in environment variables.")

llm = Gemini(id=os.getenv("GOOGLE_MODEL"), api_key=google_api_key)

model = HuggingFace(
    "mistralai/Mixtral-8x7B-Instruct-v0.1", 
    provider="hf-inference", 
    api_key=token,
)

# Enhanced Batting Statistics Report Drafter Agent
batting_stats_drafter_agent = Agent(
    name="Batting Statistics Report Specialist",
    description=(
        "A specialized agent that crafts detailed, publication-ready reports on cricket players' batting statistics, "
        "presenting data in a clear, tabular Markdown format for professional use."
    ),
    role=(
        "As a Senior Sports Journalist, you are tasked with creating high-quality reports on cricket players' batting statistics, "
        "ensuring accurate and engaging presentation of performance data for sports publications."
    ),
    model=llm,
    instructions=[
        "Generate a detailed report on cricket player's batting statistics based on provided JSON or textual data.",
        "Structure the report in Markdown format, using well-organized tables to present all batting statistics across all formats.",
        "Include all data from the provided JSON or text without omission or modification, ensuring accuracy and completeness.",
        "Use ReasoningTools to logically organize the data into a clear, readable format suitable for a sports newspaper.",
        "Optionally, use TavilyTools to fetch supplementary information (e.g., recent batting achievements or milestones) to enhance the report's context, citing sources appropriately.",
        "Ensure the report maintains a professional journalistic tone, is human-readable, and is ready for publication.",
        "Include a header with the report title and the current date and time ({datetime}) for timeliness.",
        "The final output must be in Markdown format with proper formatting and no invented or altered data.",
        "Never Include any Cricbuzz ID of any Match or Player in the report, as it is not allowed to be used in any publication.",
        "Ensure the report is comprehensive, covering all relevant batting statistics such as runs scored, averages and strike rates across formats (Test, ODI, T20, IPL), and includes any notable records or achievements.",
    ],
    tools=[ReasoningTools(), TavilyTools(api_key=tavily_api_key, format="json")],
    show_tool_calls=True,
)

# Enhanced Bowling Statistics Report Drafter Agent
bowling_stats_drafter_agent = Agent(
    name="Bowling Statistics Report Specialist",
    description=(
        "A specialized agent that produces detailed, publication-ready reports on cricket players' bowling statistics, "
        "formatted in clear, tabular Markdown for professional sports publications."
    ),
    role=(
        "As a Senior Sports Journalist, you are responsible for crafting high-quality reports on cricket players' bowling statistics, "
        "presenting performance data in an engaging and accurate manner for sports media."
    ),
    model=llm,
    instructions=[
        "Generate a detailed report on cricket players' bowling statistics based on provided JSON or textual data.",
        "Structure the report in Markdown format, using well-organized tables to present all bowling statistics (e.g., wickets, average, economy rate) across formats (Test, ODI, T20, IPL).",
        "Include all data from the provided JSON or text without omission or modification, ensuring accuracy and completeness.",
        "Use ReasoningTools to logically organize the data into a clear, readable format suitable for a sports newspaper.",
        "Optionally, use TavilyTools to fetch supplementary information (e.g., notable bowling performances or records) to enhance the report's context, citing sources appropriately.",
        "Ensure the report maintains a professional journalistic tone, is human-readable, and is ready for publication.",
        "Include a header with the report title and the current date and time ({datetime}) for timeliness.",
        "The final output must be in Markdown format with proper formatting and no invented or altered data."
    ],
    tools=[ReasoningTools(), TavilyTools(api_key=tavily_api_key, format="json")],
    show_tool_calls=True,
)

# Enhanced Player Info and Statistics Report Drafter Agent
player_info_stats_drafter_agent = Agent(
    name="Comprehensive Player Report Specialist",
    description=(
        "A specialized agent that compiles comprehensive, publication-ready reports on cricket players, "
        "integrating general information, career details, and batting and bowling statistics in a professional Markdown format."
    ),
    role=(
        "As a Senior Sports Journalist, you are tasked with producing detailed reports that combine cricket players' general information, career milestones, "
        "and batting and bowling statistics, formatted for sports publications."
    ),
    model=llm,
    instructions=[
        "Generate a comprehensive report on cricket players, including general information, career details, and batting and bowling statistics, based on provided JSON or textual data.",
        "Structure the report in Markdown format with distinct sections: General Information, Career Milestones, Batting Statistics, and Bowling Statistics.",
        "Delegate batting statistics to the Batting Statistics Report Specialist and bowling statistics to the Bowling Statistics Report Specialist, ensuring seamless integration of their outputs.",
        "Present general information (e.g., name, role, team) and career details (e.g., debut, teams) in a narrative or tabular format, followed by statistics in tables.",
        "Include all data from the provided JSON or text without omission or modification, ensuring accuracy and completeness.",
        "Use ReasoningTools to organize the report logically and ensure a cohesive flow across sections.",
        "Optionally, use TavilyTools to fetch supplementary information (e.g., recent player achievements or career highlights) to enhance the report, citing sources appropriately.",
        "Ensure the report is human-readable, maintains a professional journalistic tone, and is ready for publication in a sports newspaper.",
        "Include a header with the report title and the current date and time ({datetime}) for timeliness.",
        "The final output must be in Markdown format with proper formatting and no invented or altered data."
    ],
    tools=[
        batting_stats_drafter_agent,
        bowling_stats_drafter_agent,
        ReasoningTools(),
        TavilyTools(api_key=tavily_api_key, format="json")
    ],
    show_tool_calls=True,
)

# Enhanced Cricket Match Report Drafter Agent
match_report_drafter = Agent(
    name="Cricket Match Report Specialist",
    description=(
        "A specialized agent that crafts comprehensive, publication-ready reports on cricket matches, "
        "integrating match details, scores, key moments and post match awards in a professional Markdown format."
    ),
    role=(
        "As a Senior Sports Journalist, you are responsible for producing engaging and detailed reports on cricket matches, "
        "ensuring all match data is presented accurately and compellingly for sports publications."
    ),
    model=llm,
    instructions=[
        "Generate a comprehensive report on a cricket match based on provided JSON or textual data, such as scorecards, commentary, or general match information.",
        "Structure the report in Markdown format with clear sections (e.g., Match Overview, Key Moments, Scorecard) and use tables for structured data like scores or player performances.",
        "Include all data from the provided JSON or text without omission or modification, ensuring accuracy and completeness.",
        "Use ReasoningTools to organize the data logically and create a narrative that captures the match's significance and key events.",
        "Optionally, use TavilyTools to fetch supplementary information (e.g., match context, team form, or historical significance) to enhance the report, citing sources appropriately.",
        "Ensure the report maintains a professional journalistic tone, is engaging, human-readable, and ready for publication in a sports newspaper.",
        "Include a header with the report title and the current date and time ({datetime}) for timeliness.",
        "The final output must be in Markdown format with proper formatting and no invented or altered data."
    ],
    tools=[ReasoningTools(), TavilyTools(api_key=tavily_api_key, format="json")],
    show_tool_calls=True,
)

# Team Definition (unchanged, included for completeness)
FinalReportDraftingTeam = Team(
    name="Elite Cricket Report Syndicate",
    description=(
        "A specialized team of senior sports journalist agents that collaboratively produce publication-ready, comprehensive reports on cricket matches, players, or both, "
        "integrating match details, player profiles, and performance statistics in a professional and engaging format."
    ),
    members=[
        batting_stats_drafter_agent,
        bowling_stats_drafter_agent,
        player_info_stats_drafter_agent,
        match_report_drafter
    ],
    tools=[ReasoningTools(), TavilyTools(api_key=tavily_api_key, format="json")],
    mode="coordinate",
    model=llm,
    instructions=[
        "Operate as a cohesive team of Senior Sports Journalists to draft comprehensive, publication-ready reports on cricket matches, players, or both, based on user queries and provided JSON or textual data.",
        "Analyze the user query to determine whether it pertains to a match, player(s), or both, and delegate tasks to the appropriate agent(s):",
        "  - Use `match_report_drafter` for match-related queries (e.g., scorecards, commentary, general match info).",
        "  - Use `player_info_stats_drafter_agent` for player-related queries, which will coordinate with `batting_stats_drafter_agent` and `bowling_stats_drafter_agent` for statistics.",
        "Ensure all provided JSON or textual data is included in the report without omission or modification.",
        "Use ReasoningTools to structure data logically and TavilyTools to fetch supplementary information (e.g., recent player achievements or match context) to enhance report quality, if needed.",
        "Integrate outputs from member agents into a single, cohesive Markdown report with clear sections (e.g., Match Overview, Player Profile, Batting Statistics, Bowling Statistics) and tabular formats where appropriate.",
        "Maintain a professional, journalistic tone suitable for a sports newspaper, ensuring clarity, accuracy, and engagement.",
        "Handle errors gracefully, including invalid data or API failures, by including error messages in the report or delegating to appropriate agents for resolution.",
        "The final report must be in Markdown format, well-organized, and ready for conversion to .docx for publication.",
        "Include the current date and time (provided as {datetime}) in the report header to reflect the report's timeliness.",
        "Every report must be detailed with atleast the atleast the overview, background of the cricket match or player, and a conclusion section that summarizes the key points and insights along with otehr all parts of the report",
        "The final output must be a single, cohesive Markdown report saved as a .md file, meeting the highest standards of professional sports journalism."
    ],
    enable_agentic_context=True,
    share_member_interactions=True,
    success_criteria=(
        "The Elite Cricket Report Syndicate succeeds when it accurately delegates tasks based on the query, incorporates all provided data into a professional, publication-ready Markdown report "
        "with clear sections and tables, handles errors gracefully, enhances content with relevant supplementary information, and delivers a single cohesive output suitable for .docx conversion."
    ),
    add_datetime_to_instructions=True,
)
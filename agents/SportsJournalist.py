from agno.agent import Agent
from agno.team.team import Team
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
import os
from dotenv import load_dotenv

# Assuming these imports are correctly defined in their respective modules
from Getting_IDs import Getting_ID_Team
from FinalDrafter import FinalReportDraftingTeam
from GetMatchDetails import cricket_data_agent
from GetPlayerStats import cricket_player_agent
from ReportSavingAgent import saving_agent
from WebAgent import Web_Search_Agent

# Load environment variables
load_dotenv("../.env")

google_api_key = os.getenv("GOOGLE_API_KEY")

# Validate environment variables
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

llm = Gemini(id=os.getenv("GOOGLE_MODEL"), api_key=google_api_key)

# Enhanced Sports Journalist Team
SportsJournalistTeam = Team(
    members=[
        Web_Search_Agent,
        Getting_ID_Team,
        cricket_data_agent,
        cricket_player_agent,
        FinalReportDraftingTeam,
        saving_agent
    ],
    name="Premier Cricket Journalism Syndicate",
    description=(
        "An internationally acclaimed team of expert AI agents and sub-teams that deliver comprehensive, publication-ready reports on cricket matches, players, or both, "
        "integrating detailed data, insightful analysis, and professional formatting for top-tier sports media."
    ),
    mode="coordinate",
    model=llm,
    tools=[ReasoningTools()],
    show_members_responses=True,  # Suppress individual member responses
    show_tool_calls=True,  # Suppress tool call logs
    markdown=True,
    instructions=[
        "Operate as an elite team of Senior Sports Journalists to produce comprehensive, detailed, publication-ready reports on cricket matches, players, or both, based on user queries and provided data, as of {datetime}.",
        "Analyze the user query to determine whether it pertains to a match, player(s), or both, and delegate tasks to the appropriate members:",
        "  - Use `Getting_ID_Team` to retrieve Cricbuzz IDs for matches or players if only names (with or without dates) are provided.",
        "  - Use `cricket_data_agent` to fetch match data (e.g., scorecards, commentary, general info) based on the match ID.",
        "  - Use `cricket_player_agent` to gather player data (e.g., batting, bowling, profile, career info) based on the player ID.",
        "  - Use `Web_Search_Agent` to fetch essential supplementary information (e.g., recent player achievements, match context, or tournament background) only when needed and not obtainable from other members, ensuring minimal web scraping.",
        "  - Use `FinalReportDraftingTeam` to draft the comprehensive report, integrating match and/or player data.",
        "  - Use `saving_agent` to save the final report as a .md file and convert it to .docx format in the `../reports/` directory. Derive the filename from the query content along with the current date and time : {datetime} (e.g., 'RCB_vs_PBKS_IPL_2025_Finals.md' for a match or 'Virat_Kohli_2025-06-24.md' for a player), extracting the match title, player name, or date from the query or report content. Sanitize filenames to remove invalid characters and append a timestamp (e.g., '_20250624191300') to avoid overwriting existing files. Prepend a header to the Markdown content with the report title (from the first H1/H2 heading or query) and the current date/time in 'YYYY-MM-DD HH:MM:SS UTC' format. Handle errors (e.g., permission issues, Pandoc failures) by including clear error messages in the report or retrying with an alternative filename.",
        "Based on the knowledge of your Team members and analysis of the user query, first always devise a plan to determine the necessary tasks and delegate them to the appropriate members, ensuring all required data is gathered before drafting the report.",
        "Include all provided JSON or textual data recievd from the team members or sub teams in the report without omission or modification, ensuring accuracy and fidelity to the original data.",
        "For match reports, include team performance, key moments, and relevant player statistics, highlighting critical events and outcomes in a narrative that captures the match's significance.",
        "For player reports, include a general profile (e.g., name, team, role), career highlights, and detailed statistics (e.g., batting runs, bowling wickets) in tabular format.",
        "For combined match and player reports, integrate match context (e.g., result, key moments) with player-specific insights (e.g., standout performances), emphasizing the player's contribution to the match.",
        "Structure the report in Markdown format with clear sections (e.g., Match Overview, Player Profile, Statistics, Analysis and Conclusion), using headers and tables for readability and publication readiness.",
        "Include a header with the report title (e.g., 'IPL 2025 Finals: RCB vs PBKS') and the current date and time ({datetime}) for timeliness.",
        "Ensure the report maintains a professional, engaging journalistic tone, suitable for publication in a top-tier sports newspaper, with a detailed analysis and conclusion section incorporating key cricket terminology.",
        "Use ReasoningTools to logically organize data and also smartly delegate tasks to members or subteams and ensure a cohesive, compelling narrative across sections.",
        "Handle errors gracefully, including invalid IDs, API failures, or missing data, by including clear error messages in the report or delegating to appropriate members for resolution.",
        "Always save the final report using `saving_agent`, ensuring the output .md and .docx files are publication-ready with preserved formatting and professional structure.",
        "Always call the `saving_agent` at the end of the report drafting process to ensure the final report is saved correctly.",
        "Make sure that the `saving_agent` is the last member to be called in the task delegation process and called only once, Do not save multiple reports.",
        "STRICTLY Make sure to pass on the entire final markdown report to the saving_agent for saving.",
        "The final output must be a single, cohesive Markdown report saved as a .md file and then as a .docx file, meeting the highest standards of professional sports journalism.",
        "Do NOT return intermediate plans, logs, or step-by-step updates in the terminal output and the report. Suppress all intermediate messages, including task delegation logs or status updates (e.g., 'Okay, I will create a report' or 'Delegating to Cricbuzz ID Finding Team').",
        "After saving the report, display only the full content of the saved Markdown report in the output, followed by a confirmation message indicating the report was saved successfully (e.g., 'Report saved successfully as Virat_Kohli_Report.md').",
        "Ensure all sub-agents complete their tasks and aggregate their outputs before returning any response to the user."
        ],
        share_member_interactions=True,
        enable_agentic_context=True,
        add_datetime_to_instructions=True,
        success_criteria=(
            """The Premier Cricket Journalism Syndicate succeeds when it accurately delegates tasks, retrieves necessary Cricbuzz IDs, incorporates all provided data, uses necessary supplementary web information,
            and delivers a professional, publication-ready Markdown report saved as a .md file and then a docx file from that md file with clear sections, tables, and an engaging, detailed journalistic narrative, displaying only the final report content and save confirmation in the terminal."""
        )
    )

if __name__ == "__main__":
    SportsJournalistTeam.print_response("Give me a report on Bowling Statistics of Trent Boult.", stream=True, markdown=True)
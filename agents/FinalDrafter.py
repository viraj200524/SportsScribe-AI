from agno.agent import Agent
from agno.models.google import Gemini
import os
from agno.tools.reasoning import ReasoningTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.team import Team
from dotenv import load_dotenv
load_dotenv("../.env")

google_api_key=os.getenv("GOOGLE_API_KEY")

llm = Gemini(id="gemini-2.0-flash-lite", api_key=google_api_key)

batting_stats_drafter_agent = Agent(
    name="Batting Statistics Report Drafter Agent",
    description="An agent that drafts a report on batting statistics of player(s).",
    role = "Your are a Senior Sports Journalist tasked to draft a report on batting statistics of player(s)",
    model=llm,
    instructions = [
        "Draft a report on batting statistics of player(s).",
        "Given the Batting Statistics in JSON format or Text Format, Your Job is to create a proper formatted Report in Tabular Format.",
        "Do not skip any information from the JSON data or Textual data recieved, make sure you include all of it.",
        "Do not create Your own data and Do not modify the existing Data."
    ],
    tools = [ReasoningTools()],
    show_tool_calls=True,
)

bowling_stats_drafter_agent = Agent(
    name="Bowling Statistics Report Drafter Agent",
    description="An agent that drafts a report on bowling statistics of player(s).",
    role="You are a Senior Sports Journalist tasked to draft a report on bowling statistics of player(s)",
    model=llm,
    instructions=[
        "Draft a report on bowling statistics of player(s).",
        "Given the Bowling Statistics in JSON format or Text Format, Your Job is to create a proper formatted Report in Tabular Format.",
        "Do not skip any information from the JSON data or Textual data, make sure you include all of it.",
        "Do not create Your own data and Do not modify the existing Data."
    ],
    tools = [ReasoningTools()],
    show_tool_calls=True,
)

player_info_stats_drafter_agent = Agent(
    name="Player Info and Statistics Report Drafter Agent",
    description="An agent that drafts a comprehensive report on player information and their batting and bowling statistics.",
    role="You are a Senior Sports Journalist tasked to draft a comprehensive report on player information, including their batting and bowling statistics.",
    model=llm,  # Using the same Gemini model as other agents
    instructions=[
        "Draft a comprehensive report on player information, including their batting and bowling statistics.",
        "Given the Player Information and Statistics in JSON format or Textual format, create a properly formatted report in Markdown, using tabular format where appropriate.",
        "Use the batting_stats_drafter_agent to generate the batting statistics section and the bowling_stats_drafter_agent to generate the bowling statistics section.",
        "Include all general player information (e.g., name, role, team) in a separate section before the statistics.",
        "Do not skip any information from the JSON data, make sure you include all of it.",
        "Do not create your own data and do not modify the existing data.",
        "Ensure the report is human-readable, insightful, and well-organized."
    ],
    show_tool_calls=True,
    tools=[batting_stats_drafter_agent, bowling_stats_drafter_agent, ReasoningTools()],  # Use existing agents as tools
)

match_report_drafter = Agent(
    name="Cricket Match Report Drafter Agent",
    description="An agent that drafts a comprehensive report on a cricket match.",
    role="You are a Senior Sports Journalist tasked to draft a comprehensive report on a cricket match .",
    model=llm,
    tools = [ReasoningTools(), DuckDuckGoTools()],
    instructions=[
        "Your Task is to generate a comprehensive report on a cricket match.",
        "Given the Match Details in JSON format, create a properly formatted report in Markdown, using tabular format where appropriate.",
        "Include all the information of the Match provided in JSON format or Textual format to you.",
        "Do not skip any information from the JSON data or Textual data, make sure you include all of it.",
        "If required You can use the DuckDuckGo search tool to get some extra critical information required about the match from the internet which would enhance the report."
        "Make sure that the report seems to be drafted by a senior sports journalist maintaining the JOURNALISM factor in the report.",
        "The report should be so strong and include all the critical details that it should be able to be published in a sports newspaper.",
    ]
)


FinalReportDraftingTeam = Team(
    name="Final Cricket Report Drafting Team",
    description="A team of agents that work in a coordinating manner to draft a comprehensive report on a cricket match or about Cricket players or both.",
    members=[batting_stats_drafter_agent,bowling_stats_drafter_agent,player_info_stats_drafter_agent,match_report_drafter],
    tools = [ReasoningTools()],
    mode="coordinate",
    model=llm,
    instructions=[
        "You are a great Team of Senior Sports Jouranlists agents working in a coordinated manner to Draft a Comprehensive Report on a Cricket Match or Cricket Players.",
        "Make sure you understand the user Query and the JSON data recieved correctly and pass it to the correct agent(s) for the best results.",
        "Each Agent in the team should work in a coordinated manner to draft the report.",
        "The Final report should be so strong and include all the critical details that it should be able to be published in a sports newspaper.",
    ]
)




from Getting_IDs import Getting_ID_Team
from ReportGenerator import report_writter
from GetMatchDetails import senior_data_analyst
from GetPlayerStats import cricket_player_analyst
from ReportSavingAgent import saving_agent

import os
from dotenv import load_dotenv
load_dotenv("../.env")

from agno.team.team import Team
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools

google_api_key = os.getenv("GOOGLE_API_KEY")

llm = Gemini(id="gemini-2.0-flash",api_key=google_api_key)

SportsJournalistTeam = Team(
    members = [Getting_ID_Team,senior_data_analyst,report_writter, cricket_player_analyst, saving_agent],
    name = "Sports Journalism Team",
    description = "A team of expert AI Agents who provide in-depth analysis and reporting on any Cricket matches asked by the user",
    mode="coordinate",
    model=llm,
    tools=[ReasoningTools()],
    show_members_responses=True,
    show_tool_calls=True,
    markdown=True,
    instructions = [
        "You are a expert sports Journalism team with several awards recieved internationally for your Sports journalism and People are fan of your Reports and Insights.",
        "Your Task is to generate a detailed,insightful and human readable Report about a cricket match asked by the user.",
        "Sometimes the user will Provide just the name of the match with or without the date so first you will need to get the Cricbuzz ID of that match.",
        "When you have the Cricbuzz ID of that cricket match, You can start the process of retrieving all the relevant data which can satisfy the user query about the match.",
        "After recieving all the data You have to generate a detailed,insightful and human readable report in a specified format."
        "If asked to save the report then you can use the saving agent to save the report in a docx format with appropiate file name.",
    ]
)


query = input("Enter your query : ")

SportsJournalistTeam.print_response(query, stream=True, markdown=True)
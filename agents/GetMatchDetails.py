import os
from dotenv import load_dotenv
import requests
from agno.models.groq import Groq
from agno.models.google import Gemini
from agno.tools import Toolkit
from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools

# Load environment variables
load_dotenv("../.env")

x_api_token = os.getenv("X-RAPID-API-KEY")
x_api_host = os.getenv("X-RAPID-API-HOST")

# Validate environment variables
if not x_api_token or not x_api_host:
    raise ValueError("X-RAPID-API-KEY or X-RAPID-API-HOST not found in environment variables.")

goog_llm = Gemini(id="gemini-2.0-flash",api_key=os.getenv("GOOGLE_API_KEY"))
groq_llm = Groq(id="llama3-70b-8192",api_key=os.getenv("GROQ_API_KEY"))

cricket_instructions = "You are an AI-powered tool that can fetch information about any cricket match using all available tools."

class CricketMatchTools(Toolkit):
    def __init__(self):
        super().__init__(
            name="Cricket Tool",
            tools=[self.get_match_score_card, self.get_match_commentary, self.get_general_match_info],
            instructions=cricket_instructions,
            add_instructions=True
        )

    def get_match_score_card(self, matchID: int) -> dict:
        """
        Fetch the complete scorecard of a specific cricket match.

        Args:
            matchID (int): Unique ID of the cricket match.

        Returns:
            dict: JSON data containing detailed scorecard information for each innings.

        Usage:
            Use this tool when you need in-depth statistics of each player’s performance in a given match.
        """
        if not isinstance(matchID, int) or matchID <= 0:
            return {"error": "Invalid matchID. Must be a positive integer."}

        url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{matchID}/scard"
        headers = {
            "x-rapidapi-key": x_api_token,
            "x-rapidapi-host": x_api_host
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}

    def get_match_commentary(self, matchID: int) -> dict:
        """
        Retrieve the live or past ball-by-ball text commentary of a cricket match.

        Args:
            matchID (int): Unique ID of the cricket match.

        Returns:
            dict: JSON data with over-wise and ball-wise commentary.

        Usage:
            Use this tool to reconstruct the flow of the match or understand key moments.
        """
        if not isinstance(matchID, int) or matchID <= 0:
            return {"error": "Invalid matchID. Must be a positive integer."}

        url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{matchID}/comm"
        headers = {
            "x-rapidapi-key": x_api_token,
            "x-rapidapi-host": x_api_host
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}

    def get_general_match_info(self, matchID: int) -> dict:
        """
        Get general metadata and high-level details about a cricket match.

        Args:
            matchID (int): Unique ID of the cricket match.

        Returns:
            dict: JSON data including teams, venue, toss result, match status, and team lineups.

        Usage:
            Use this tool to extract contextual and logistical information about the match.
        """
        if not isinstance(matchID, int) or matchID <= 0:
            return {"error": "Invalid matchID. Must be a positive integer."}

        url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{matchID}"
        headers = {
            "x-rapidapi-key": x_api_token,
            "x-rapidapi-host": x_api_host
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}

senior_data_analyst = Agent(
    name="Cricket Match Analyst",
    model=goog_llm,
    role="Senior Cricket Analyst, acting as a data retriever.",
    description=(
        "A cricket data agent that fetches raw JSON data about any cricket match using a given matchID. "
        "It can retrieve scorecards, commentary, and general match info, but does not analyze or summarize the data."
    ),
    tools=[CricketMatchTools(),ReasoningTools()],
    instructions="""
Your job is to retrieve and return raw JSON data about cricket matches based on the matchID provided by the user.

You have access to the following tools:

1. **get_match_score_card(matchID: int)**: Fetch the full match scorecard.
2. **get_match_commentary(matchID: int)**: Fetch over-wise and ball-by-ball match commentary.
3. **get_general_match_info(matchID: int)**: Fetch general details like teams, venue, toss, and status.

🛠 Your response must:
- ONLY call the relevant tool(s) based on the user request.
- Return the data in proper json formatting as recieved from the api and beutify it a bit if required to make the json more readable.
- Do NOT interpret, summarize, or explain the data.
- If the user specifies which data they want (e.g., “get me scorecard for matchID 123”), call only that tool.
- Always pretty print the json

🧠 Example queries:
- "Give me the scorecard of match ID 45063"
- "Fetch commentary for match ID 99500"
- "Get general info about match 67320"

Only use tools. Do not generate natural language explanations.
"""
)

# Execute the query
if __name__ == "__main__":
    senior_data_analyst.print_response("Give me the general info of the cricket match with ID 115192")
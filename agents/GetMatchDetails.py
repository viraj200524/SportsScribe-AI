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
google_api_key = os.getenv("GOOGLE_API_KEY")

# Validate environment variables
if not x_api_token or not x_api_host:
    raise ValueError("X-RAPID-API-KEY or X-RAPID-API-HOST not found in environment variables.")

goog_llm = Gemini(id=os.getenv("GOOGLE_MODEL"),api_key=google_api_key)
groq_llm = Groq(id="llama3-70b-8192",api_key=os.getenv("GROQ_API_KEY"))

cricket_instructions = "You are an AI-powered tool that can fetch information about any cricket match, given the cricket match ID using all available tools."

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

cricket_data_agent = Agent(
    name="Cricket Data Fetcher",
    model=goog_llm,
    role="Cricket Data Specialist",
    description=(
        "An agent designed to fetch raw JSON data for cricket matches using a provided match ID. "
        "It retrieves scorecards, ball-by-ball commentary, or general match information without analyzing or summarizing the data."
    ),
    tools=[CricketMatchTools(), ReasoningTools()],
    instructions="""
        Your role is to fetch JSON data for cricket matches based on the matchID provided by the user, using the CricketMatchTools toolkit.

        Available tools:
        1. **get_match_score_card(matchID: int)**: Retrieves the full match scorecard with detailed player statistics.
        2. **get_match_commentary(matchID: int)**: Fetches over-wise and ball-by-ball match commentary.
        3. **get_general_match_info(matchID: int)**: Obtains general match details such as teams, venue, toss result, and status.

        Response requirements:
        - Call only the tool(s) specified by the user's request (e.g., scorecard, commentary, or general info).
        - You can use the ReasontingTools to reason about ambiguios user requests and determine the most suitable tool to call.
        - Return the raw JSON data as received from the API, formatted with proper indentation for readability.
        - Do NOT analyze, summarize, or provide explanations of the data.
        - If the user specifies a particular type of data (e.g., "get scorecard for matchID 123"), use only the corresponding tool.
        - Pretty-print the JSON output using json.dumps with an indent of 2 for clarity.

        Example queries:
        - "Fetch the scorecard for match ID 45063"
        - "Get commentary for match ID 99500"
        - "Retrieve general info for match ID 67320"

        Use only the provided tools and return only the JSON data.
        """
)
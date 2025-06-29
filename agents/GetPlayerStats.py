from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.tools import Toolkit
from agno.tools.reasoning import ReasoningTools
import os
import requests
from dotenv import load_dotenv
load_dotenv("../.env")

google_api_key = os.getenv("GOOGLE_API_KEY")
x_rapidapi_key=os.getenv("X-RAPID-API-KEY")
x_rapidapi_host=os.getenv("X-RAPID-API-HOST")

cricket_instructions = "You are an AI-powered tool that can fetch information about any cricket player given the player ID by using all the available tools to the full potential."

from agno.agent import Toolkit
import requests

class CricketPlayerTool(Toolkit):
    def __init__(self):
        super().__init__(name="Cricket Player Tool", tools=[self.get_player_batting_stats, self.get_player_bowling_stats, self.get_player_info, self.get_player_career_info], instructions=cricket_instructions, add_instructions=True)

    def get_player_batting_stats(self, playerID: int) -> dict:
        """
        Fetch batting statistics for a specific cricket player.

        Args:
            playerID (int): Unique ID of the cricket player.

        Returns:
            dict: JSON data containing batting statistics across formats (Test, ODI, T20, IPL).

        Usage:
            Use this tool to retrieve detailed batting performance metrics, such as runs, average, and strike rate.
        """
        if not isinstance(playerID, int) or playerID <= 0:
            return {"error": "Invalid playerID. Must be a positive integer."}

        url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{playerID}/batting"
        headers = {
            "x-rapidapi-key": x_rapidapi_key,
            "x-rapidapi-host": x_rapidapi_host
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}

    def get_player_bowling_stats(self, playerID: int) -> dict:
        """
        Fetch bowling statistics for a specific cricket player.

        Args:
            playerID (int): Unique ID of the cricket player.

        Returns:
            dict: JSON data containing bowling statistics across formats (Test, ODI, T20, IPL).

        Usage:
            Use this tool to retrieve detailed bowling performance metrics, such as wickets, average, and economy rate.
        """
        if not isinstance(playerID, int) or playerID <= 0:
            return {"error": "Invalid playerID. Must be a positive integer."}

        url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{playerID}/bowling"
        headers = {
            "x-rapidapi-key": x_rapidapi_key,
            "x-rapidapi-host": x_rapidapi_host
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}

    def get_player_info(self, playerID: int) -> dict:
        """
        Fetch profile information for a specific cricket player.

        Args:
            playerID (int): Unique ID of the cricket player.

        Returns:
            dict: JSON data including name, date of birth, role, batting style, and bowling style.

        Usage:
            Use this tool to extract personal and professional details about the player.
        """
        if not isinstance(playerID, int) or playerID <= 0:
            return {"error": "Invalid playerID. Must be a positive integer."}

        url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{playerID}"
        headers = {
            "x-rapidapi-key": x_rapidapi_key,
            "x-rapidapi-host": x_rapidapi_host
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}

    def get_player_career_info(self, playerID: int) -> dict:
        """
        Fetch career information for a specific cricket player.

        Args:
            playerID (int): Unique ID of the cricket player.

        Returns:
            dict: JSON data including teams, debut matches, and last matches across formats.

        Usage:
            Use this tool to extract career milestones and team affiliations for the player.
        """
        if not isinstance(playerID, int) or playerID <= 0:
            return {"error": "Invalid playerID. Must be a positive integer."}

        url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{playerID}/career"
        headers = {
            "x-rapidapi-key": x_rapidapi_key,
            "x-rapidapi-host": x_rapidapi_host
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
        

cricket_player_agent = Agent(
    name="Cricket Player Data Fetcher",
    model=Gemini(id=os.getenv("GOOGLE_MODEL1"), api_key=google_api_key),
    role="Cricket Player Data Specialist",
    description=(
        "An agent designed to fetch raw JSON data for cricket players using a provided player ID. "
        "It retrieves batting statistics, bowling statistics, profile information, or career details without analyzing or summarizing the data."
    ),
    tools=[CricketPlayerTool(), ReasoningTools()],
    instructions="""
        Your role is to fetch raw JSON data for cricket players based on the playerID provided by the user, using the CricketPlayerTool toolkit.

        Available tools in CricketPlayerTool:
        1. **get_player_batting_stats(playerID: int)**: Retrieves batting statistics across formats.
        2. **get_player_bowling_stats(playerID: int)**: Fetches bowling statistics across formats.
        3. **get_player_info(playerID: int)**: Obtains profile details such as name, date of birth, role, batting style, and bowling style.
        4. **get_player_career_info(playerID: int)**: Retrieves career details including teams, debut matches, and last matches.

        Response requirements:
        - Call only the tool(s) specified by the user's request (e.g., batting stats, bowling stats, profile, or career info).
        - Do not call any tool that is not relevant to the user's request.
        - Return the raw JSON data as received from the API.
        - You can use the ReasontingTools to reason about ambiguios user requests and determine the most suitable tool to call.
        - Do NOT analyze, summarize, or provide explanations of the data.
        - If the user specifies a particular type of data (e.g., "get batting stats for playerID 123"), use only the corresponding tool.
        - Ensure the output is as it is recieved from the tool, without any modifications or additional formatting.

        Example queries:
        - "Fetch batting stats for player ID 35320"
        - "Get bowling statistics for player ID 625383"
        - "Retrieve profile info for player ID 28081"
        - "Get career info for player ID 253802"

        Use only the provided tools and return only the JSON data.
        """,
)
    


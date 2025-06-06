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
groq_api_key=os.getenv("GROQ_API_KEY")
x_rapidapi_key=os.getenv("X-RAPID-API-KEY")
x_rapidapi_host=os.getenv("X-RAPID-API-HOST")

cricket_instructions = "You are an AI-powered tool that can fetch information about any cricket match using all available tools."

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
        

cricket_player_analyst = Agent(
    name="Cricket Player Analyst",
    model=Gemini(id="gemini-2.0-flash"),
    role="Senior Cricket Analyst, acting as a data retriever.",
    description=(
        "A cricket data agent that fetches raw JSON data about any cricket player using a given playerID. "
        "It can retrieve batting statistics, bowling statistics, profile information, and career details, but does not analyze or summarize the data."
    ),
    tools=[CricketPlayerTool(), ReasoningTools()],
    instructions="""
Your job is to retrieve and return raw JSON data about cricket players based on the playerID provided by the user.

You have access to the following tools:

1. **get_player_batting_stats(playerID: int)**: Fetch the player's batting statistics across formats.
2. **get_player_bowling_stats(playerID: int)**: Fetch the player's bowling statistics across formats.
3. **get_player_info(playerID: int)**: Fetch general profile details like name, role, and styles.
4. **get_player_career_info(playerID: int)**: Fetch career details like teams, debut, and last matches.

🛠 Your response must:
- ONLY call the relevant tool(s) based on the user request.
- If asked for batting stats then display the Output in Proper Tabular Format.
- If asked for bowling stats then display the Output in Proper Tabular Format.
- If asked for Career info of the player then display the output in a Formal Report Format.
- If asked for Player Info then display the output in a Formal Report Format.
- Do NOT interpret, summarize, or explain the data.
- If the user specifies which data they want (e.g., “get me batting stats for playerID 1413”), call only that tool.
- If the API returns an error, include the error message in the JSON output as received, maintaining the pretty-printed format.

🧠 Example queries:
- "Give me the batting stats of player ID 1413"
- "Fetch career info for player ID 576"
- "Get general info about player 35263"

Only use tools. Do not generate natural language explanations.
"""
)

if __name__ == "__main__":
    cricket_player_analyst.print_response("Give me info of the player with ID 1413")
    
    


from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import markdown
from SportsJournalist import SportsJournalistTeam as agent
from Getting_IDs import Getting_ID_Team as id_agent
from GetPlayerStats import cricket_player_agent as player_agent

app = FastAPI()

# Define a Pydantic model to handle the JSON input
class ReportRequest(BaseModel):
    input: str

# Basic CSS for formatting the HTML preview
HTML_CSS = """
<style>
    body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; color: #333; }
    h1 { font-size: 24px; color: #2c3e50; }
    h2 { font-size: 20px; color: #34495e; }
    p { font-size: 16px; margin: 10px 0; }
    ul, ol { margin: 15px 0; padding-left: 30px; }
    li { margin-bottom: 8px; }
    code { background: #f4f4f4; padding: 2px 4px; border-radius: 4px; }
    pre { background: #f4f4f4; padding: 10px; border-radius: 4px; overflow-x: auto; }
    table { border-collapse: collapse; width: 100%; margin: 15px 0; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background: #f4f4f4; }
</style>
"""

@app.post("/get_report", response_class=HTMLResponse)
async def get_report(request: ReportRequest):
    try:
        # Assuming agent.run returns a markdown string
        markdown_content = agent.run(message=request.input).content
        if not markdown_content:
            return HTMLResponse(
                content="<h1>Error</h1><p>No report generated. Please check your input or try again.</p>",
                status_code=400
            )
        
        # Convert markdown to HTML
        html_content = markdown.markdown(markdown_content, extensions=['extra', 'tables'])
        
        # Combine HTML with CSS
        full_html = f"<html><head>{HTML_CSS}</head><body>{html_content}</body></html>"
        
        # Return HTML response
        return HTMLResponse(content=full_html)
    except Exception as e:
        return HTMLResponse(
            content=f"<h1>Error</h1><p>{str(e)}</p>",
            status_code=500
        )
    
@app.post("/get_batting", response_class=JSONResponse)
async def get_batting(request: ReportRequest):
    try:
        # Run agent and get output
        id_response = id_agent.run(message=request.input)

        agent_prompt = f"Get the batting stats for the player with ID: {id_response.content}"

        agent_response = player_agent.run(message=agent_prompt)

        # If the content is a JSON string, parse it
        if isinstance(agent_response.content, str):
            import json
            parsed_json = json.loads(agent_response.content)
        else:
            parsed_json = agent_response.content  # already a dict or list

        return JSONResponse(content=parsed_json)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@app.post("/get_bowling", response_class=JSONResponse)
async def get_batting(request: ReportRequest):
    try:
        # Run agent and get output
        id_response = id_agent.run(message=request.input)

        agent_prompt = f"Get the bowling stats for the player with ID: {id_response.content}"

        agent_response = player_agent.run(message=agent_prompt)

        # If the content is a JSON string, parse it
        if isinstance(agent_response.content, str):
            import json
            parsed_json = json.loads(agent_response.content)
        else:
            parsed_json = agent_response.content  # already a dict or list

        return JSONResponse(content=parsed_json)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
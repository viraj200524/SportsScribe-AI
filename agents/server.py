from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import markdown
from SportsJournalist import SportsJournalistTeam as agent
from Getting_IDs import Getting_ID_Team as id_agent
from GetPlayerStats import cricket_player_agent as player_agent
from ReportSavingAgent import get_file_path
import json
import ast
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
import os
from report_narration import narrate_cricket_report
import shutil

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

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
        id_response = id_agent.run(message=request.input)
        print(f"id_response.content: {id_response.content}")  # Debugging line
        agent_prompt = f"""Given the response of the Cricbuzz ID finding agent, get the batting statistics for the player with that ID:
                        Response of the ID finding agent: {id_response.content}"""

        agent_response = player_agent.run(message=agent_prompt)
        cleaned = agent_response.content.strip("`").split("\n", 1)[-1].rsplit("\n", 1)[0].replace("'",'"')
        print(f"agent_response.content: {cleaned}")  # Debugging line
        if isinstance(cleaned, str):
            outer_json = json.loads(cleaned)  
        else:
            outer_json = cleaned  
        result_str = outer_json.get("get_player_batting_stats_response", {}).get("result")
        if not result_str:
            return JSONResponse(
                content={"error": "No 'result' field found in response"},
                status_code=400
            )
        try:
            parsed_result = ast.literal_eval(result_str)
        except (ValueError, SyntaxError) as e:
            try:
                fixed_result_str = result_str.replace("'", '"')
                parsed_result = json.loads(fixed_result_str)
            except json.JSONDecodeError as json_err:
                return JSONResponse(
                    content={"error": f"Failed to parse result: {str(json_err)}"},
                    status_code=400
                )
        return JSONResponse(content=parsed_result)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@app.post("/get_bowling", response_class=JSONResponse)
async def get_bowling(request: ReportRequest):
    try:
        id_response = id_agent.run(message=request.input)
        print(f"id_response.content: {id_response.content}")  # Debugging line
        agent_prompt = f"""Given the response of the Cricbuzz ID finding agent, get the bowling statistics for the player with that ID:
                        Response of the ID finding agent: {id_response.content}"""

        agent_response = player_agent.run(message=agent_prompt)
        cleaned = agent_response.content.strip("`").split("\n", 1)[-1].rsplit("\n", 1)[0].replace("'",'"')
        print(f"agent_response.content: {cleaned}")  # Debugging line
        if isinstance(cleaned, str):
            outer_json = json.loads(cleaned)  
        else:
            outer_json = cleaned  
        result_str = outer_json.get("get_player_bowling_stats_response", {}).get("result")
        if not result_str:
            return JSONResponse(
                content={"error": "No 'result' field found in response"},
                status_code=400
            )
        try:
            parsed_result = ast.literal_eval(result_str)
        except (ValueError, SyntaxError) as e:
            try:
                fixed_result_str = result_str.replace("'", '"')
                parsed_result = json.loads(fixed_result_str)
            except json.JSONDecodeError as json_err:
                return JSONResponse(
                    content={"error": f"Failed to parse result: {str(json_err)}"},
                    status_code=400
                )
        return JSONResponse(content=parsed_result)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@app.get("/download-docx")
def download_docx():
    filepath = get_file_path()
    filename = os.path.basename(filepath)
    return FileResponse(
        path=filepath,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

class SpeechResponse(BaseModel):
    text: str | None = None
    error: str | None = None

# Ensure audio directory exists
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

class MarkdownInput(BaseModel):
    content: str  # Markdown content string

@app.post("/generate-narration-audio")
async def generate_narration_audio(data: MarkdownInput):
    try:
        audio_filename = narrate_cricket_report(data.content)
        saved_path = os.path.join(AUDIO_DIR, audio_filename)

        # Move generated file to audio folder
        if os.path.exists(audio_filename):
            shutil.move(audio_filename, saved_path)
        else:
            raise FileNotFoundError("Audio file not generated.")

        # Return downloadable/streamable link
        return {
            "audio_url": f"/audio/{audio_filename}",
            "filename": audio_filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve audio files from the /audio/ path
@app.get("/audio/{filename}", response_class=FileResponse)
async def serve_audio_file(filename: str):
    file_path = os.path.join(AUDIO_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mp3", filename=filename)
    raise HTTPException(status_code=404, detail="Audio file not found.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

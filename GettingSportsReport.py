from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from agents.SportsJournalist import SportsJournalistTeam  # Assuming this is your custom module

app = FastAPI()

# Define a Pydantic model to handle the JSON input
class ReportRequest(BaseModel):
    input: str

@app.post("/get_report")
async def get_report(request: ReportRequest):
    try:
        response = SportsJournalistTeam.run(message=request.input)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
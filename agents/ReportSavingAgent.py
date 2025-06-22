from agno.agent import Agent
from agno.tools import tool
from agno.models.google import Gemini
import os
from dotenv import load_dotenv
from pathlib import Path
import markdown
from docx import Document

# Load environment variables
load_dotenv("../.env")
google_api_key = os.getenv("GOOGLE_API_KEY")

# Validate environment variables
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

# Base directory for saving reports
base_directory = Path("../reports/")

@tool
def write_file(filename: str, markdown_report: str) -> None:
    """
    Saves a the markdown report in a proper formatted .md file.

    Args:
        filename (str): Name of the output Word document (without extension).
        report (str): Markdown-formatted text to be converted.

    Returns:
        A statement indicating the success or failure of the save operation.
    """
    # Ensure base directory exists
    base_dir = base_directory
    os.makedirs(base_dir, exist_ok=True)

    if not filename.endswith(".md"):
        filename += ".md"
    
    filepath = os.path.join(base_dir, filename)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(markdown_report)
    
    return f"Markdown report saved to {filepath}"


# Enhanced Saving Agent
saving_agent = Agent(
    name="Cricket Report Archivist",
    description=(
        "A specialized agent that saves cricket reports in markdown format"
        "ensuring human-readable presentation and proper file management for publication purposes."
    ),
    role=(
        "As a Senior Sports Archivist, you are responsible for saving cricket reports in well-formatted markdown format."
        "preserving the integrity of the provided Markdown content and ensuring accessibility for sports publications."
    ),
    tools=[write_file],
    show_tool_calls=True,
    model=Gemini(id="gemini-2.0-flash-lite", api_key=google_api_key),
    instructions=[
        "Save provided cricket reports (in Markdown format) as professionally formatted .md files in the base directory (../reports/).",
        "Use the write_file tool to process the report, ensuring the filename is appropriate (e.g., based on the report's content, such as player name or match ID) and includes the .md extension.",
        "Preserve all provided Markdown content without modification, converting it to a human-readable .md format with proper headings, paragraphs, and tables as defined by the Markdown structure.",
        "Ensure the base directory exists and overwrite existing files with the same name to prevent duplication.",
        "Include a header in the .md file with the report title (if present in the Markdown) and the current date and time ({datetime}) for timeliness.",
        "Handle errors gracefully, returning clear feedback (e.g., 'Error saving report: [error message]') if file saving fails due to permissions, invalid paths, or other issues.",
        "Maintain a professional approach, ensuring the saved .docx file is ready for publication or distribution in a sports journalism context.",
        "The final output is the success or error message returned by the write_file tool, indicating the result of the save operation."
    ]
)
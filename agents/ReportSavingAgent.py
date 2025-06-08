from agno.agent import Agent
from agno.tools import tool
from agno.models.google import Gemini
import os
from dotenv import load_dotenv
from pathlib import Path
import markdown
from markdown import markdown as md_to_html
from docx import Document
from docx.shared import Pt
from docx.enum.style import WD_STYLE_TYPE
import re
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv("../.env")
google_api_key = os.getenv("GOOGLE_API_KEY")

# Validate environment variables
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

# Base directory for saving reports
base_directory = Path("../reports/")

@tool
def write_file(filename: str, report: str) -> str:
    """
    Create or overwrite a .docx file in the base directory with the provided report content,
    formatted in a human-readable way.

    Args:
        filename (str): Name of the file to write (e.g., 'report'). Will append .docx if not present.
        report (str): Report content in markdown format to write to the file.

    Returns:
        str: Success or error message indicating the result of the operation.
    """
    try:
        # Ensure filename has .docx extension
        if not filename.lower().endswith('.docx'):
            filename += '.docx'

        # Convert base_dir to Path object
        base_dir_path = Path(base_directory)
        
        # Ensure the base directory exists
        base_dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create full file path
        file_path = base_dir_path / filename

        # Convert markdown to HTML
        html_content = md_to_html(report, extensions=['extra', 'fenced_code'])

        # Parse HTML to extract content for .docx
        soup = BeautifulSoup(html_content, 'html.parser')

        # Create a new Document
        doc = Document()

        # Define basic styles for better formatting
        styles = doc.styles
        if 'Normal' in styles:
            styles['Normal'].font.name = 'Arial'
            styles['Normal'].font.size = Pt(11)

        # Add title (assuming first h1 or h2 as title)
        title = soup.find(['h1', 'h2'])
        if title:
            doc.add_heading(title.get_text(), level=1).style.font.size = Pt(16)

        # Process other elements
        for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol', 'li', 'code']):
            if element.name in ['h1', 'h2']:
                doc.add_heading(element.get_text(), level=1 if element.name == 'h1' else 2)
            elif element.name == 'h3':
                doc.add_heading(element.get_text(), level=3)
            elif element.name == 'p':
                doc.add_paragraph(element.get_text())
            elif element.name in ['ul', 'ol']:
                for li in element.find_all('li'):
                    para = doc.add_paragraph(element.get_text(), style='ListBullet' if element.name == 'ul' else 'ListNumber')
            elif element.name == 'code':
                para = doc.add_paragraph()
                run = para.add_run(element.get_text())
                run.font.name = 'Courier New'
                run.font.size = Pt(10)

        # Save the document
        doc.save(file_path)
        return f"Report successfully saved to {file_path}"

    except Exception as e:
        return f"Error saving report: {str(e)}"

# Enhanced Saving Agent
saving_agent = Agent(
    name="Cricket Report Archivist",
    description=(
        "A specialized agent that saves cricket reports in professionally formatted .docx files, "
        "ensuring human-readable presentation and proper file management for publication purposes."
    ),
    role=(
        "As a Senior Sports Archivist, you are responsible for saving cricket reports in well-formatted .docx files, "
        "preserving the integrity of the provided Markdown content and ensuring accessibility for sports publications."
    ),
    tools=[write_file],
    show_tool_calls=True,
    model=Gemini(id="gemini-2.0-flash-lite", api_key=google_api_key),
    instructions=[
        "Save provided cricket reports (in Markdown format) as professionally formatted .docx files in the base directory (../reports/).",
        "Use the write_file tool to process the report, ensuring the filename is appropriate (e.g., based on the report’s content, such as player name or match ID) and includes the .docx extension.",
        "Preserve all provided Markdown content without modification, converting it to a human-readable .docx format with proper headings, paragraphs, and tables as defined by the Markdown structure.",
        "Ensure the base directory exists and overwrite existing files with the same name to prevent duplication.",
        "Include a header in the .docx file with the report title (if present in the Markdown) and the current date and time ({datetime}) for timeliness.",
        "Handle errors gracefully, returning clear feedback (e.g., 'Error saving report: [error message]') if file saving fails due to permissions, invalid paths, or other issues.",
        "Maintain a professional approach, ensuring the saved .docx file is ready for publication or distribution in a sports journalism context.",
        "The final output is the success or error message returned by the write_file tool, indicating the result of the save operation."
    ]
)
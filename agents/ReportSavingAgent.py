from agno.agent import Agent
from agno.tools import tool
from agno.models.google import Gemini
import os
from dotenv import load_dotenv
from pathlib import Path
import markdown
from docx import Document
import pypandoc
from datetime import datetime
import re

report_filepath = ""

# Load environment variables
load_dotenv("../.env")
google_api_key = os.getenv("GOOGLE_API_KEY")

# Validate environment variables
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

# Base directory for saving reports
base_directory = Path("../reports/")

def md_to_docx_with_pandoc(md_file_path, output_path):
    """
    Converts a Markdown file to a DOCX file using Pandoc.

    Args:
        md_file_path (str): Path to the input Markdown file.
        output_path (str): Path where the DOCX file will be saved.

    Raises:
        RuntimeError: If Pandoc conversion fails or Pandoc is not installed.
        OSError: If file operations encounter permission or path issues.

    Returns:
        None: Prints a success message upon completion.
    """
    try:
        pypandoc.convert_file(md_file_path, 'docx', outputfile=output_path)
        print(f"Saved DOCX to {output_path}")
    except pypandoc.PandocError as e:
        raise RuntimeError(f"Pandoc conversion failed: {str(e)}")
    except OSError as e:
        raise OSError(f"File operation failed: {str(e)}")

@tool
def write_file(filename: str, markdown_report: str) -> str:
    """
    Saves a cricket report in Markdown format as a .md file and converts it to DOCX.

    The function ensures the report is saved in the base directory (`../reports/`), creates the directory if it doesn't exist,
    and sanitizes the filename to prevent invalid characters. It also converts the Markdown file to DOCX using Pandoc.

    Args:
        filename (str): Desired filename for the report (without extension). If no .md extension is provided, it is appended.
                        Invalid characters are replaced with underscores.
        markdown_report (str): Markdown-formatted report content to be saved.

    Returns:
        str: A message indicating success (e.g., "Markdown report saved to [filepath] and converted to .docx format.")
             or an error message if the operation fails.

    Raises:
        ValueError: If markdown_report is empty or invalid.
        OSError: If file writing or directory creation fails due to permissions or invalid paths.
        RuntimeError: If Pandoc conversion fails.

    Example:
        >>> write_file("match_123", "# Match Report\nDetails here.")
        "Markdown report saved to ../reports/match_123.md and converted to .docx format."
    """
    try:
        # Validate input
        if not markdown_report.strip():
            raise ValueError("Markdown report cannot be empty.")

        # Sanitize filename
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename.strip())
        if not filename.endswith(".md"):
            filename += ".md"

        # Ensure base directory exists
        base_dir = base_directory
        base_dir.mkdir(parents=True, exist_ok=True)

        # Construct filepath
        filepath = base_dir / filename

        # Write Markdown file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(markdown_report)

        # Convert to DOCX
        docx_path = filepath.with_suffix(".docx")
        md_to_docx_with_pandoc(filepath, str(docx_path))

        global report_filepath
        report_filepath = str(docx_path)

        return f"Markdown report saved to {filepath} and converted to .docx format."

    except ValueError as e:
        return f"Error saving report: {str(e)}"
    except OSError as e:
        return f"Error saving report: File operation failed - {str(e)}"
    except RuntimeError as e:
        return f"Error saving report: {str(e)}"
    
def get_file_path() -> str:
    """
    Returns the path of the last saved report file.

    This function retrieves the global variable `report_filepath`, which is set during the file writing process.

    Returns:
        str: The path of the last saved report file, or an empty string if no file has been saved yet.
    """
    return report_filepath if report_filepath else "../reports/Indian_Batsmen_Batting_Statistics_and_T20_Recommendation.docx"

# Enhanced Saving Agent
saving_agent = Agent(
    name="Cricket Report Archivist",
    description=(
        "A specialized agent designed to strictly preserve and save entire cricket reports in their original Markdown format, "
        "ensuring no content is altered, omitted, or modified, and converting them to DOCX for publication."
    ),
    role=(
        "As a Senior Sports Archivist, you are responsible for saving cricket reports in their exact, unmodified Markdown format "
        "as .md files and ensuring their accurate conversion to DOCX, maintaining all original content, formatting, and structure."
    ),
    tools=[write_file],
    show_tool_calls=True,
    model=Gemini(id=os.getenv("GOOGLE_MODEL"), api_key=google_api_key),
    instructions=[
        "Save the entire provided cricket report in its original Markdown format as a .md file in the base directory (`../reports/`).",
        "Use the `write_file` tool to save the report exactly as received, without modifying, summarizing, or omitting any content, and convert it to DOCX.",
        "Ensure the filename matches the report's identifier (e.g., player name, match ID, or title extracted from the first H1 or H2 heading). If no identifier is present, use 'cricket_report_{timestamp}' with the format 'YYYYMMDDHHMMSS'.",
        "Prepend a header to the Markdown content with the report title (extracted from the first H1 or H2 heading, if present) and the current date/time in the format 'YYYY-MM-DD HH:MM:SS UTC' (e.g., '2025-06-24 19:13:00 UTC'), ensuring the original report content remains unchanged below the header.",
        "Preserve all Markdown elements (headings, paragraphs, lists, tables, etc.) exactly as provided, ensuring identical rendering in both .md and .docx outputs.",
        "Sanitize filenames to remove invalid characters and prevent path issues.",
        "Avoid overwriting existing files unless explicitly instructed; append a timestamp (e.g., '_20250624191300') to the filename to resolve conflicts.",
        "Handle errors gracefully, returning clear feedback via the `write_file` tool (e.g., 'Error saving report: Permission denied'). Expected errors include permission issues, invalid paths, or Pandoc conversion failures.",
        "Ensure the output .docx file accurately reflects the original Markdown content, with all formatting preserved for publication.",
        "Return only the success or error message from the `write_file` tool as the final output."
    ]
)
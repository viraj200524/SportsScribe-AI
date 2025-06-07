from agno.agent import Agent
from agno.tools import tool
from agno.models.groq import Groq
import os
from dotenv import load_dotenv
load_dotenv("../.env")

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

saving_instructions = ["Given Some content to save, Create a file with appropiate file name in the base directory specified and write the content as it is into it, Do not make any changes to it.",
                       "Do not generate any content of your Own."
                       "Make sure you always save reports in docx format i.e. with the extension of .docx",
                       "If the Text contains Markdown Content, then first write it in markdown then save in .docx file"]

from pathlib import Path

base_dir = Path("../reports/")

@tool
def write_file(filename: str, contents: str, base_dir: str) -> None:
    """
    Check if a file exists in the base directory, overwrite it if it exists,
    or create a new file, then write the contents to it.

    Args:
        filename (str): Name of the file to write (e.g., 'report.docx').
        contents (str): Content to write to the file.
        base_dir (str): Base directory path where the file will be saved.
    """
    # Convert base_dir to Path object
    base_dir_path = Path(base_dir)
    
    # Ensure the base directory exists
    base_dir_path.mkdir(parents=True, exist_ok=True)
    
    # Create full file path
    file_path = base_dir_path / filename
    
    # Write contents to the file (overwrites if exists, creates if not)
    with file_path.open('w', encoding='utf-8') as f:
        f.write(contents)

saving_agent = Agent(
    name="Report Saving Agent",
    role="You are simple report saving agent",
    description="Your task is to save the content given in a docx file report with appropriate name in the base directory",
    tools=[write_file],
    show_tool_calls=True, 
    model=Groq(id="llama3-70b-8192"),
    instructions=saving_instructions,
)
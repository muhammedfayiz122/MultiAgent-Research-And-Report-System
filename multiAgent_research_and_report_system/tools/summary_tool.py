from langchain_core.tools import tool
from typing import Annotated
from pathlib import Path

WORKING_DIRECTORY = Path(__file__).parent.parent.parent / "summaries"
WORKING_DIRECTORY.mkdir(parents=True, exist_ok=True)

@tool
def create_summary(
    content: Annotated[str, "Research content to summarize"],
    file_name: Annotated[str, "File path to save the summary"],
) -> Annotated[str, "Path of the saved summary file"]:
    """Create and save a summary from research content."""
    # Ensure the file has a .txt extension for summaries
    
    
    
    if not file_name.endswith(('.txt', '.md')):
        file_name = file_name.rsplit(".", 1)[0] + ".txt" if "." in file_name else file_name + ".txt"
    
    file_path = WORKING_DIRECTORY / file_name
    with file_path.open("w", encoding='utf-8') as file:
        file.write(content)
    return f"Summary saved to {file_path}"
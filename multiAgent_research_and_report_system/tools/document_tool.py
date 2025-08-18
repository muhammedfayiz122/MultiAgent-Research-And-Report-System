from langchain_core.tools import tool
from typing import Annotated
from pathlib import Path

WORKING_DIRECTORY = Path(__file__).parent.parent.parent / "sessions"
print(WORKING_DIRECTORY)
WORKING_DIRECTORY.mkdir(parents=True, exist_ok=True)

@tool
def create_document(
    content: Annotated[str, "Content to be written into the document"],
    file_name: Annotated[str, "File path to save the document"],
) -> Annotated[str, "Path of the saved document file"]:
    """Create and save a document from summary content as a Markdown file."""
    # Ensure the file has a .md extension for Markdown documents
    if not file_name.endswith(".md"):
        file_name = file_name.rsplit(".", 1)[0] + ".md" if "." in file_name else file_name + ".md"
    
    file_path = WORKING_DIRECTORY / file_name
    with file_path.open("w", encoding='utf-8') as file:
        file.write(content)
    return f"Document saved to {file_path}"
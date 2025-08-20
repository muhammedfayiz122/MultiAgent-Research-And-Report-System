from langchain_core.tools import tool
from typing import Annotated, Optional
from pathlib import Path

WORKING_DIRECTORY = Path(__file__).parent.parent.parent / "session"

@tool
def read_file(
    file_name: Annotated[str, "name of the file to read with extension"],
    ) -> str:
    """Read report file from the working directory."""
    try:
        file_path = WORKING_DIRECTORY / file_name
        with file_path.open("r", encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return f"File {file_name} not found in {WORKING_DIRECTORY}"
    except Exception as e:
        return f"Error reading file {file_name}: {str(e)}"

@tool
def write_file(
    file_name: Annotated[str, "File name to store as file "],
    content: Annotated[str, "Content to be written into the document"] = ""
) -> Annotated[str, "Path of the saved document file"]:
    """Create and save a document from summary content."""
    try:
        # Determine file path
        file_path = WORKING_DIRECTORY / file_name

        # Create parent directories if they don't exist
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write content to the file
        with file_path.open("w", encoding='utf-8') as file:
            file.write(content)
            
        return f"Document saved to {file_path}"
    except Exception as e:
        return f"error writing into file : {e}"
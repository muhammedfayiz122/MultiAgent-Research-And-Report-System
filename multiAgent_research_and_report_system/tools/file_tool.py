from langchain_core.tools import tool
from typing import Annotated
from pathlib import Path

WORKING_DIRECTORY = Path(__file__).parent.parent.parent / "summaries"
WORKING_DIRECTORY.mkdir(parents=True, exist_ok=True)
FILE_NAME = "report.txt"

@tool
def read_file() -> str:
    """Read report file from the working directory."""
    try:
        file_path = WORKING_DIRECTORY / FILE_NAME
        with file_path.open("r", encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return f"File {FILE_NAME} not found in {WORKING_DIRECTORY}"
    except Exception as e:
        return f"Error reading file {FILE_NAME}: {str(e)}"
    
@tool
def write_file(
    content: Annotated[str, "Content to be written into the document"]
) -> Annotated[str, "Path of the saved document file"]:
    """Create and save a document from summary content."""
    try:
        file_path = WORKING_DIRECTORY / FILE_NAME
        with file_path.open("w", encoding='utf-8') as file:
            file.write(content)
        return f"Document saved to {file_path}"
    except Exception as e:
        return f"error writing into file : {e}"
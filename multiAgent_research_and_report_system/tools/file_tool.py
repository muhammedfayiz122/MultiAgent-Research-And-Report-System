from langchain_core.tools import tool
from typing import Annotated
from pathlib import Path

WORKING_DIRECTORY = Path(__file__).parent.parent.parent / "summaries"
WORKING_DIRECTORY.mkdir(parents=True, exist_ok=True)

@tool
def read_file(
    file_name: Annotated[str, "File path to read"],
) -> str:
    """Read the specified file from the working directory."""
    try:
        file_path = WORKING_DIRECTORY / file_name
        with file_path.open("r", encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return f"File {file_name} not found in {WORKING_DIRECTORY}"
    except Exception as e:
        return f"Error reading file {file_name}: {str(e)}"
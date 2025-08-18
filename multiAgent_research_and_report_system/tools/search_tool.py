from langchain_core.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv
import os

load_dotenv()
serper_api_key = os.environ.get("SERPER_API_KEY")

@tool
def enhanced_search(query: str, search_type: str = "search") -> str:
    """Enhanced search using Serper for real-time data and current information."""
    try:
        serper_search = GoogleSerperAPIWrapper(serper_api_key=serper_api_key)
        results = serper_search.results(query)
        formatted_content = []
        
        if 'organic' in results:
            for i, result in enumerate(results['organic'][:8], 1):
                content = f"<Source {i}>\n"
                content += f"Title: {result.get('title', 'N/A')}\n"
                content += f"URL: {result.get('link', 'N/A')}\n"
                content += f"Snippet: {result.get('snippet', 'N/A')}\n"
                content += f"Date: {result.get('date', 'Recent')}\n"
                content += "</Source>\n"
                formatted_content.append(content)
        
        if 'news' in results:
            formatted_content.append("\n<Recent News>\n")
            for i, news in enumerate(results['news'][:3], 1):
                content = f"News {i}: {news.get('title', 'N/A')}\n"
                content += f"Source: {news.get('source', 'N/A')}\n"
                content += f"Date: {news.get('date', 'Recent')}\n"
                content += f"Summary: {news.get('snippet', 'N/A')}\n\n"
                formatted_content.append(content)
            formatted_content.append("</Recent News>\n")
        
        return "\n".join(formatted_content) if formatted_content else "No results found"
    except Exception as e:
        return f"Search error: {str(e)}"

if __name__ == "__main__":
    # Run a test search
    query = "latest news on AI"
    print(enhanced_search.invoke(query))
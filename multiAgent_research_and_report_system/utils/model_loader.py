from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

def model_loader(api_key=None):
    if api_key:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=api_key)
    else:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    return llm

if __name__ == "__main__":
    llm = model_loader(api_key)
    llm.invoke("hi")

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from tavily import TavilyClient
from typing import Dict, Any
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = init_chat_model(model="gpt-5.4-mini")

@tool("web_search", description="Search the web for recipes based on ingredients")
def web_search(query: str) -> Dict[str, Any]:
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = client.search(query)
    return response

system_prompt = """
You are a personal chef. User will give you list of ingredients that they have in their kitchen.

Using the web search tool, search the web for recipes that can be made with the given ingredients. 

Return a list of recipes with their names, ingredients, and share instructions if asked.
"""

agent = create_agent(model=llm, tools=[web_search], system_prompt=system_prompt)
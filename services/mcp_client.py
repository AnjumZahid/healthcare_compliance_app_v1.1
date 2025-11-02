# client.py
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv

load_dotenv()

async def query_fda(drug_name: str) -> str:
    """
    Query FDA MCP tool for drug information
    """
    client = MultiServerMCPClient({
        "fda": {
            "url": "http://localhost:8002/mcp",
            "transport": "streamable_http",
        }
    })
    tools = await client.get_tools()
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    agent = create_react_agent(model, tools)

    response = await agent.ainvoke({
        "messages": [
            {"role": "user", "content": f"Get FDA info for {drug_name}"}
        ]
    })

    return response["messages"][-1].content



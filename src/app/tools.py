import logging
from mcp.server.fastmcp import FastMCP
import chromadb

"""
Ferramentas para a IA utlizar
"""


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fatec-mcp")


mcp = FastMCP("fatec-docs", json_response=True)


@mcp.tool()
async def list_all() -> list[dict]:
    return [
        {
            "id": doc["id"]
        } 
        for doc in localstack_list
    ]

@mcp.tool()
async def search() -> list[dict]:
    return [
        {
            "content": doc["content"]
        } 
        for doc in vetorial_db
    ]

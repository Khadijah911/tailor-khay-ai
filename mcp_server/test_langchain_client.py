import asyncio
import sys
from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():

    client = MultiServerMCPClient(
        {
            "tailor_khay": {
                "transport": "stdio",
                "command": sys.executable,
                "args": ["-m", "mcp_server.server"],
            }
        }
    )

    tools = await client.get_tools()

    print("Available LangChain tools:")

    for tool in tools:
        print("-", tool.name)


if __name__ == "__main__":
    asyncio.run(main())
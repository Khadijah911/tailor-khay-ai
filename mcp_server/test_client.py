import anyio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


server_params = StdioServerParameters(
    command="python",
    args=["-m", "mcp_server.server"],
)


async def main():
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:

            await session.initialize()

            tools = await session.list_tools()

            print("Available tools:")
            for tool in tools.tools:
                print("-", tool.name)

            result = await session.call_tool(
                "check_calendar",
                {
                    "date": "2026-08-10",
                    "time": "10:00"
                }
            )

            print("\nTool result:")
            print(result)
            print(result.content)


if __name__ == "__main__":
    anyio.run(main)
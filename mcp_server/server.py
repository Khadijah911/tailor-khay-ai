from mcp.server import Server
from mcp import types
from mcp.server.stdio import stdio_server
import anyio
import json
from mcp_server.calendar_tools import check_calendar,book_appointment

server = Server("tailor-khay")


@server.list_tools()
async def list_tools():
    return [
        types.Tool(
            name="check_calendar",
            description="Check whether an appointment slot is available.",
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Appointment date in YYYY-MM-DD format."
                    },
                    "time": {
                        "type": "string",
                        "description": "Appointment time in HH:MM format."
                    }
                },
                "required": ["date", "time"],
            },
        ),
        types.Tool(
            name="book_appointment",
            description="Book a customer appointment.",
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {"type": "string"},
                    "time": {"type": "string"},
                    "customer_name": {"type": "string"},
                    "phone_number": {"type": "string"},
                    "purpose": {"type": "string"},
                },
                "required": [
                    "date",
                    "time",
                    "customer_name",
                    "phone_number",
                    "purpose",
                ],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name, arguments):

    if name == "check_calendar":
        result = check_calendar(
            arguments["date"],
            arguments["time"]
        )

        return [
            types.TextContent(
                type="text",
                text=json.dumps(result)
            )
        ]

    if name == "book_appointment":
        result = book_appointment(
            arguments["date"],
            arguments["time"],
            arguments["customer_name"],
            arguments["phone_number"],
            arguments["purpose"]
        )

        return [
            types.TextContent(
                type="text",
                text=json.dumps(result)
            )
        ]
    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    anyio.run(main)
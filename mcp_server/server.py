from mcp.server import MCPServer
import anyio

from mcp_server.calendar_tools import (
    check_calendar,
    book_appointment,
)

server = MCPServer("tailor-khay")


@server.tool(
    name="check_calendar",
    description="Check whether a specific appointment slot is available."
)
def check_calendar_tool(date: str, time: str) -> dict:
    return check_calendar(date, time)


@server.tool(
    name="book_appointment",
    description="Book a customer appointment."
)
def book_appointment_tool(
    date: str,
    time: str,
    customer_name: str,
    phone_number: str,
    purpose: str,
) -> dict:
    return book_appointment(
        date,
        time,
        customer_name,
        phone_number,
        purpose,
    )


async def main():
    await server.run_stdio_async()


if __name__ == "__main__":
    anyio.run(main)
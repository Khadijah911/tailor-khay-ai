#from mcp.server import 
from mcp.server.fastmcp import FastMCP
import anyio

from mcp_server.calendar_tools import (
    check_calendar,
    book_appointment,cancel_appointment,view_appointments
)

#server = MCPServer("tailor-khay")
server = FastMCP("tailor-khay")


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

@server.tool(
    name="cancel_appointment",
    description="CANCEL a customer's appointment."
)

def cancel_appointment_tool(
    phone_number: str,
    customer_name: str) -> dict:
    return cancel_appointment(
        phone_number,
        customer_name
    )

@server.tool(
    name="view_appointments",
    description="VIEW  customer's appointment."
)

def view_appointments_tool(
    date:str) -> dict:
    return view_appointments(
        date 
    )



async def main():
    await server.run_stdio_async()


if __name__ == "__main__":
    anyio.run(main)
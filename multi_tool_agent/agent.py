import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

def get_biographies(name: str) -> dict:
    """Retrieves the biographies from a open source media"""

    Args:
        name (str): The name of the politician for which to retrieve the biographie.

    Returns:
        dict: a sintentized biographie of the given politician.   

    """
    if name.lower() == "Pedro Sanchez":
        return {
            "status": "success",
            "report": (
                "Pedro Sanchez, was born in ... on ....  He as politician from PSOE"
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f" The is no information available for '{name}'"

    """

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


root_agent = Agent(
    name="biographical_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to generate politicians biographies"
    ),
    instruction=(
        "You are agent specialized in generating up to date politicians biographies",
    tools=[get_biographies, get_from_different_sources],
)

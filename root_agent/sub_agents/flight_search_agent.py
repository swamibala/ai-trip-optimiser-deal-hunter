from google.adk.agents import Agent
from root_agent.tools import search_flight

flight_search_agent = Agent(
    name="FlightSearchAgent",
    model="gemini-2.5-flash-lite",
    instruction="""You are a Flight Search Agent. User has already provided travel preferences in {user_preferences}.
    Do not ask more followup questions to the user. Just use the flight search tool to find suitable flight options.
    You SHOULD use IATA airport code for the departure and arrival cities. If there are multiple IATA codes for a city, choose the most popular one.""",
    tools=[search_flight],
    output_key="flight_options",
)

print("✅ flight_search_agent created.")

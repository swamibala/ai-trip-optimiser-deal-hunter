from google.adk.agents import Agent
from root_agent.tools import search_flight

flight_search_agent = Agent(
    name="FlightSearchAgent",
    model="gemini-2.5-flash-lite",
    instruction="""You are a Flight Search Agent. Read user input about their travel preferences from {user_preferences}.
    You will use the flight search tools to find suitable flight options based on user preferences.""",
    tools=[search_flight],
    output_key="flight_options",
)

print("✅ flight_search_agent created.")

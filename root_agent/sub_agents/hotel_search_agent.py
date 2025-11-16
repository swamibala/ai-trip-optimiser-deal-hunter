from google.adk.agents import Agent
from root_agent.tools import search_hotels


hotel_search_agent = Agent(
    name="HotelSearchAgent",
    model="gemini-2.5-flash-lite",
    instruction="""You are a Hotel Search Agent. Read user input about their travel preferences from {user_preferences}.
    You will use the hotel search tools to find suitable hotel options based on user preferences.""",
    tools=[search_hotels],
    output_key="hotel_options",
)

print("✅ hotel_search_agent created.")
